#User Management
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.audit.rbac_audit import RBACAudit
from app.audit.user_audit import UserAudit
from app.core.security import hash_password
from app.errors.auth import (
    EmailAlreadyUsedError,
    PermissionDeniedError,
    RoleAlreadyAssignedError,
    RoleNotFoundError,
    RoleProtectedError,
    UsernameAlreadyUsedError,
    UserNotFoundError,
)
from app.models.roles import Role
from app.models.user_customers import UserCustomer
from app.models.user_roles import UserRole
from app.models.users import User
from app.repositories.role_repository import role_repository
from app.repositories.user_repository import user_repository
from app.schemas.user import (
    UserCreate,
    UserDetailRead,
    UserRead,
    UserRoleUpdate,
    UserUpdate,
)


class UserService:
    async def get_all(self, db: AsyncSession, user_id: UUID) -> list[UserRead]:
        role_names = set(await user_repository.get_role_names(db, user_id))

        result = []
        if "SUPERADMIN" in role_names:
            get_users = await user_repository.get_all_with_roles(db)
        else:
            get_users = await user_repository.get_all_with_roles(
                db,
                exclude_roles=["SUPERADMIN", "ADMIN"],
            )

        if not get_users:
            return []

        else:

            for user in get_users:
                roles = [
                    user_role.role.name
                    for user_role in user.user_roles
                    if user_role.role
                ]

                if not roles:
                    raise RoleNotFoundError()

                result.append(
                    UserRead(
                        id=user.id,
                        username=user.username,
                        full_name=user.full_name,
                        roles=roles,
                        is_active=user.is_active,
                    )
                )

            return result

    async def get_detail(self, db: AsyncSession, user_id : UUID) -> UserDetailRead:
        user = await user_repository.get_by_id(db, user_id)

        if not user:
            raise UserNotFoundError()

        else:
            roles = []
            
            role_by_user = await db.execute(
                select(UserRole).where(user.id == UserRole.user_id)
            )

            get_role_by_user = role_by_user.scalars().all()

            if not get_role_by_user:
                raise RoleNotFoundError()

            else :

                for role_user in get_role_by_user:
                    get_role = await db.execute(
                        select(Role.name).where(Role.id == role_user.role_id)
                    )

                    role = get_role.scalar()

                    if not role:
                        raise RoleNotFoundError()
                    
                    roles.append(role)
                
            result = UserDetailRead(
                id = user.id,
                username = user.username,
                email = user.email,
                full_name = user.full_name,
                roles = roles,
                is_active = user.is_active
            )

            return result

    async def create(self, db: AsyncSession, payload: UserCreate, current_user: User) -> UserDetailRead:
        existing_email = await user_repository.get_by_email(db, payload.email)

        if existing_email:
            raise EmailAlreadyUsedError()

        existing_username = await user_repository.get_by_username(db, payload.username)

        if existing_username:
            raise UsernameAlreadyUsedError()

        role = await role_repository.get_by_id(db, payload.role_id)

        if not role:
            raise RoleNotFoundError()

        current_roles = set(await user_repository.get_role_names(db,current_user.id))

        if "SUPERADMIN" in current_roles:
            if role.name == "SUPERADMIN":
                raise PermissionDeniedError()

        elif "ADMIN" in current_roles:
            if role.name in {"ADMIN", "SUPERADMIN"}:
                raise PermissionDeniedError()

        else:
            raise PermissionDeniedError()

        set_user = UserCreate(
            username = payload.username,
            email = payload.email,
            full_name = payload.full_name,
            password = payload.password,
            role_id = role.id,
            phone_number = payload.phone_number,
            address = payload.address,
            company_name = payload.company_name,
        )

        user = User(
            username = set_user.username,
            email = set_user.email,
            full_name = set_user.full_name,
            password_hash = hash_password(set_user.password),
            is_active = True
        )

        db.add(user)
        await db.flush()

        user_role = UserRole(
            user_id = user.id,
            role_id = set_user.role_id,
            assigned_by = current_user.id
        )

        db.add(user_role)

        if role.name == "CUSTOMER":
            user_customer = UserCustomer(
            user_id = user.id,
            phone_number = set_user.phone_number,
            address = set_user.address,
            company_name = set_user.company_name
            )

            db.add(user_customer)

        user_audit = UserAudit(db)

        await user_audit.create(
            actor_id=current_user.id,
            user_id=user.id,
            username=user.username,
            role_name=role.name,
        )

        await db.commit()

        role_name = []
        role_name.append(role.name)

        result = UserDetailRead(
            id = user.id,
            username = user.username,
            email = user.email,
            full_name = user.full_name,
            roles = role_name,
            is_active = user.is_active
        )

        return result

    async def update(self, db: AsyncSession, payload: UserUpdate, current_user: User, user_id: UUID) -> UserDetailRead:

        existing_user = await user_repository.get_by_id(db, user_id)

        updated_fields = []

        if not existing_user:
            raise UserNotFoundError()

        if payload.email is not None:
            email_exist = await user_repository.get_by_email_excluding_id(db, payload.email, user_id)

            if email_exist:
                raise EmailAlreadyUsedError()

            existing_user.email = payload.email
            updated_fields.append("email")

        if payload.username is not None:
            username_exist = await user_repository.get_by_username_excluding_id(db, payload.username, user_id)

            if username_exist:
                raise UsernameAlreadyUsedError()

            existing_user.username = payload.username
            updated_fields.append("username")

        if payload.full_name is not None:
            existing_user.full_name = payload.full_name
            updated_fields.append("full_name")

        if payload.password is not None:
            existing_user.password_hash = hash_password(
                payload.password
            )
            updated_fields.append("password")

        if payload.phone_number is not None:
            existing_user.customer_profile.phone_number = payload.phone_number
            updated_fields.append("phone_number")

        if payload.address is not None:
            existing_user.customer_profile.address = payload.address

        if payload.company_name is not None:
            existing_user.customer_profile.company_name = payload.company_name

        user_audit = UserAudit(db)

        await user_audit.update(
            actor_id=current_user.id,
            user_id=existing_user.id,
            username=existing_user.username,
            updated_fields=updated_fields,
        )

        await db.commit()
        await db.refresh(existing_user)

        roles = await user_repository.get_role_names(db, existing_user.id)

        return UserDetailRead(
            id=existing_user.id,
            username=existing_user.username,
            email=existing_user.email,
            full_name=existing_user.full_name,
            roles=roles,
            is_active=existing_user.is_active
        )

    async def update_userrole(self, db: AsyncSession, payload: UserRoleUpdate, current_user: User, user_id: UUID) -> UserDetailRead:

        existing_user = await user_repository.get_by_id(db, user_id)

        if not existing_user:
            raise UserNotFoundError()

        role = await role_repository.get_by_id(db, payload.role_id)

        if not role:
            raise RoleNotFoundError()

        current_roles = set(await user_repository.get_role_names(db, current_user.id))

        if "SUPERADMIN" in current_roles:
            if role.name == "SUPERADMIN":
                raise PermissionDeniedError()

        elif "ADMIN" in current_roles:
            if role.name in {"ADMIN", "SUPERADMIN"}:
                raise PermissionDeniedError()

        else:
            raise PermissionDeniedError()

        user_role = await user_repository.get_user_role(db, existing_user.id)

        if not user_role:
            raise RoleNotFoundError()

        if user_role.role_id == role.id:
            raise RoleAlreadyAssignedError()

        before = {
            "role_id": str(user_role.role_id),
        }

        user_role.role_id = role.id
        user_role.assigned_by = current_user.id

        after = {
            "role_id": str(role.id),
        }

        rbac_audit = RBACAudit(
            db=db,
            actor_id=current_user.id,
            target_id=existing_user.id,
            target_type="USER",
        )

        await rbac_audit.assign_role(
            role_name=role.name,
            before=before,
            after=after,
        )

        await db.commit()
        await db.refresh(existing_user)

        roles = await user_repository.get_role_names(db, existing_user.id)

        return UserDetailRead(
            id=existing_user.id,
            username=existing_user.username,
            email=existing_user.email,
            full_name=existing_user.full_name,
            roles=roles,
            is_active=existing_user.is_active
        )

    async def remove(self, db: AsyncSession, user_id: UUID, current_user: User) -> User:

        user = await user_repository.get_by_id_for_update(db, user_id)

        if not user:
            raise UserNotFoundError()

        roles = await user_repository.get_role_names(db, user_id)

        if "ADMIN" in roles or "SUPERADMIN" in roles:
            raise RoleProtectedError()

        user.is_active = False

        user_audit = UserAudit(db)

        await user_audit.deactivate(
            actor_id=current_user.id,
            user_id=user.id,
            username=user.username,
        )

        await db.commit()
        await db.refresh(user)

        return {
            "user" : user,
            "message": f"{user.username} telah dinonaktifkan."
        }

    async def block(self, db: AsyncSession, user_id: UUID, current_user: User) -> User:

        user = await user_repository.get_by_id_for_update(db, user_id)

        if not user:
            raise UserNotFoundError()

        roles = await user_repository.get_role_names(db, user_id)

        if "ADMIN" in roles or "SUPERADMIN" in roles:
            raise RoleProtectedError()

        user.is_block = True

        user_audit = UserAudit(db)

        await user_audit.block(
            actor_id=current_user.id,
            user_id=user.id,
            username=user.username,
        )

        await db.commit()
        await db.refresh(user)

        return {
            "user" : user,
            "message" : f"{user.username} telah diblokir."
        }

    async def restore(self, db: AsyncSession, user_id: UUID, current_user: User) -> User:

        user = await user_repository.get_by_id_for_update(db, user_id)

        if not user:
            raise UserNotFoundError()

        roles = await user_repository.get_role_names(db, user_id)

        if "ADMIN" in roles or "SUPERADMIN" in roles:
            raise RoleProtectedError()

        user.is_active = True

        user_audit = UserAudit(db)

        await user_audit.reactivate(
            actor_id=current_user.id,
            user_id=user.id,
            username=user.username,
        )

        await db.commit()
        await db.refresh(user)

        return {
            "user" : user,
            "message": f"{user.username} telah diaktifkan kembali."
        }

    async def unblock(self, db: AsyncSession, user_id: UUID, current_user: User) -> User:

        user = await user_repository.get_by_id_for_update(db, user_id)

        if not user:
            raise UserNotFoundError()

        roles = await user_repository.get_role_names(db, user_id)

        if "ADMIN" in roles or "SUPERADMIN" in roles:
            raise RoleProtectedError()

        user.is_block = False

        user_audit = UserAudit(db)

        await user_audit.unblock(
            actor_id=current_user.id,
            user_id=user.id,
            username=user.username,
        )

        await db.commit()
        await db.refresh(user)

        return {
            "user" : user,
            "message" : f"{user.username} telah dibuka blokir."
        }


user_service = UserService()