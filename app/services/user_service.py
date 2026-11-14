#User Management
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import User
from app.models.user_roles import UserRole
from app.models.roles import Role
from app.models.user_customers import UserCustomer
from app.schemas.user import UserRead, UserDetailRead, UserCreate, UserUpdate, UserRoleUpdate

from app.errors.auth import (
    RoleNotFoundError,
    UserNotFoundError,
    EmailAlreadyUsedError,
    UsernameAlreadyUsedError,
    RoleProtectedError,
    RoleNotAllowDoubleError,
    RoleAlreadyAssignedError,
    PermissionDeniedError
)

from uuid import UUID
from app.core.security import hash_password

async def get_all_users(db: AsyncSession, user_id: UUID) -> list[UserRead]:
    statement = (select(Role.name).join(UserRole, UserRole.role_id == Role.id).where(UserRole.user_id == user_id))
    result = await db.scalars(statement)
    role_names = set(result.all())

    result = []
    if "SUPERADMIN" in role_names :
        get_now = await db.execute(select(User))
    else:
        get_now = await db.execute(
                    select(User)
                    .join(UserRole, UserRole.user_id == User.id).
                    join(Role, Role.id == UserRole.role_id)
                    .where(Role.name.not_in(["SUPERADMIN", "ADMIN"]))
        )

    get_users = get_now.scalars().all()

    if not get_users:
        return []

    else:

        for user in get_users:
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

            result.append(
                UserRead(
                    id = user.id,
                    username = user.username,
                    full_name = user.full_name,
                    roles = roles,
                    is_active = user.is_active)
            )

        return result

async def get_detail_user(db: AsyncSession, user_id : UUID) -> UserDetailRead:
    get_now = await db.execute(
        select(User).where(User.id == user_id)
    )

    user = get_now.scalar_one_or_none()

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

async def create_user_one(db: AsyncSession, payload: UserCreate, current_user: User) -> UserDetailRead:
    get_email = await db.execute(
        select(User.email).where(User.email == payload.email)
    )

    existing_email = get_email.scalar_one_or_none()

    if existing_email:
        raise EmailAlreadyUsedError()

    get_username = await db.execute(
        select(User.username).where(User.username == payload.username)
    )

    existing_username = get_username.scalar_one_or_none()

    if existing_username:
        raise UsernameAlreadyUsedError()

    get_role = await db.execute(
        select(Role).where(Role.id == payload.role_id)
    )

    role = get_role.scalar_one_or_none()

    if not role:
        raise RoleNotFoundError()

    get_current_roles = await db.execute(
        select(Role.name)
        .join(UserRole, UserRole.role_id == Role.id)
        .where(UserRole.user_id == current_user.id)
    )

    current_roles = set(get_current_roles.scalars().all())

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

async def update_user_one(db: AsyncSession, payload: UserUpdate, current_user: User, user_id: UUID) -> UserDetailRead:

    get_user = await db.execute(
        select(User).where(User.id == user_id)
    )

    existing_user = get_user.scalar_one_or_none()

    if not existing_user:
        raise UserNotFoundError()

    if payload.email is not None:
        get_email = await db.execute(
            select(User).where(
                User.email == payload.email,
                User.id != user_id
            )
        )

        email_exist = get_email.scalar_one_or_none()

        if email_exist:
            raise EmailAlreadyUsedError()

        existing_user.email = payload.email

    if payload.username is not None:
        get_username = await db.execute(
            select(User).where(
                User.username == payload.username,
                User.id != user_id
            )
        )

        username_exist = get_username.scalar_one_or_none()

        if username_exist:
            raise UsernameAlreadyUsedError()

        existing_user.username = payload.username

    if payload.full_name is not None:
        existing_user.full_name = payload.full_name

    if payload.password is not None:
        existing_user.password_hash = hash_password(
            payload.password
        )

    if payload.phone_number is not None:
        existing_user.customer_profile.phone_number = payload.phone_number

    if payload.address is not None:
        existing_user.customer_profile.address = payload.address

    if payload.company_name is not None:
        existing_user.customer_profile.company_name = payload.company_name

    await db.commit()
    await db.refresh(existing_user)

    get_roles = await db.execute(
        select(Role.name)
        .join(UserRole, UserRole.role_id == Role.id)
        .where(UserRole.user_id == existing_user.id)
    )

    roles = get_roles.scalars().all()

    return UserDetailRead(
        id=existing_user.id,
        username=existing_user.username,
        email=existing_user.email,
        full_name=existing_user.full_name,
        roles=roles,
        is_active=existing_user.is_active
    )

async def update_user_role_one(
    db: AsyncSession,
    payload: UserRoleUpdate,
    current_user: User,
    user_id: UUID,
) -> UserDetailRead:

    get_user = await db.execute(
        select(User).where(User.id == user_id)
    )

    existing_user = get_user.scalar_one_or_none()

    if not existing_user:
        raise UserNotFoundError()

    get_role = await db.execute(
        select(Role).where(Role.id == payload.role_id)
    )

    role = get_role.scalar_one_or_none()

    if not role:
        raise RoleNotFoundError()

    get_current_roles = await db.execute(
        select(Role.name)
        .join(UserRole, UserRole.role_id == Role.id)
        .where(UserRole.user_id == current_user.id)
    )

    current_roles = set(get_current_roles.scalars().all())

    if "SUPERADMIN" in current_roles:
        if role.name == "SUPERADMIN":
            raise PermissionDeniedError()

    elif "ADMIN" in current_roles:
        if role.name in {"ADMIN", "SUPERADMIN"}:
            raise PermissionDeniedError()

    else:
        raise PermissionDeniedError()

    get_user_role = await db.execute(
        select(UserRole).where(
            UserRole.user_id == existing_user.id
        )
    )

    user_role = get_user_role.scalar_one_or_none()

    if not user_role:
        raise RoleNotFoundError()

    if user_role.role_id == role.id:
        raise RoleAlreadyAssignedError()

    user_role.role_id = role.id
    user_role.assigned_by = current_user.id

    await db.commit()
    await db.refresh(existing_user)

    get_roles = await db.execute(
        select(Role.name)
        .join(UserRole, UserRole.role_id == Role.id)
        .where(UserRole.user_id == existing_user.id)
    )

    roles = get_roles.scalars().all()

    return UserDetailRead(
        id=existing_user.id,
        username=existing_user.username,
        email=existing_user.email,
        full_name=existing_user.full_name,
        roles=roles,
        is_active=existing_user.is_active
    )

async def remove_user(db: AsyncSession, user_id: UUID,
) -> User:

    get_user = await db.execute(
        select(User)
        .where(User.id == user_id)
        .with_for_update()
    )

    user = get_user.scalar_one_or_none()

    if not user:
        raise UserNotFoundError()

    get_roles = await db.execute(
        select(Role.name)
        .join(UserRole, UserRole.role_id == Role.id)
        .where(UserRole.user_id == user_id)
    )

    roles = get_roles.scalars().all()

    if "ADMIN" in roles or "SUPERADMIN" in roles:
        raise RoleProtectedError()

    user.is_active = False

    await db.commit()
    await db.refresh(user)

    return user

# async def block_user(
#     db: AsyncSession,
#     user_id: UUID,
# ) -> User:

#     get_user = await db.execute(
#         select(User)
#         .where(User.id == user_id)
#         .with_for_update()
#     )

#     user = get_user.scalar_one_or_none()

#     if not user:
#         raise UserNotFoundError()

#     get_roles = await db.execute(
#         select(Role.name)
#         .join(UserRole, UserRole.role_id == Role.id)
#         .where(UserRole.user_id == user_id)
#     )

#     roles = get_roles.scalars().all()

#     if "ADMIN" in roles or "SUPERADMIN" in roles:
#         raise RoleProtectedError()

#     user.is_blocked = True

#     await db.commit()
#     await db.refresh(user)

#     return user