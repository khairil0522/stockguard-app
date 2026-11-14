from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_password, create_access_token, hash_password
from app.models.users import User
from app.models.roles import Role
from app.models.user_customers import UserCustomer
from app.models.user_roles import UserRole
from app.errors.auth import InvalidUsernamePasswordError, UsernameAlreadyUsedError, EmailAlreadyUsedError, RoleNotFoundError
from app.schemas.auth import RegisterRequest, RegisterResponse

from app.services.audit_log_service import AuditLogService

class AuthService:
    async def login(self, db: AsyncSession, username: str, password: str):
        statement = select(User).where(User.username == username)
        user = await db.scalar(statement)

        if not user:
            await AuditLogService.log(
                db,
                actor_type="SYSTEM",
                event_type="SECURITY",
                action="LOGIN_FAILED",
                entity_type="USER",
                description="Login failed: invalid username or password",
                severity="LOW",
                event_metadata={
                    "username": username,
                },
            )

            await db.commit()
            raise InvalidUsernamePasswordError()

        if not verify_password(password, user.password_hash):
            await AuditLogService.log(
                db,
                actor_type="USER",
                user_id=user.id,
                event_type="SECURITY",
                action="LOGIN_FAILED",
                entity_type="USER",
                entity_id=user.id,
                description="Login failed: invalid username or password",
                severity="LOW",
                event_metadata={
                    "username": username,
                },
            )

            await db.commit()
            raise InvalidUsernamePasswordError()

        access_token = create_access_token(str(user.id))

        await AuditLogService.log(
            db,
            actor_type="USER",
            user_id=user.id,
            event_type="SECURITY",
            action="LOGIN_SUCCESS",
            entity_type="USER",
            entity_id=user.id,
            description=f"User {user.username} logged in successfully",
            severity="INFO",
        )

        await db.commit()

        return access_token

    async def register(self, db: AsyncSession, payload : RegisterRequest) -> RegisterResponse : #customer
        async with db.begin():
            existing_username = await db.scalar(
                select(User).where(User.username == payload.username)
            )

            if existing_username:
                raise UsernameAlreadyUsedError()

            existing_email = await db.scalar(
                select(User).where(User.email == payload.email)
            )

            if existing_email:
                raise EmailAlreadyUsedError()

            registers = User(
                username=payload.username,
                email=payload.email,
                full_name=payload.full_name,
                password_hash=hash_password(payload.password),
                is_active=True
            )

            db.add(registers)
            await db.flush()

            get_role_id = await db.scalar(
                select(Role.id).where(Role.name == "CUSTOMER")
            )

            if not get_role_id:
                raise RoleNotFoundError()

            user_role = UserRole(
                user_id = registers.id,
                role_id = get_role_id
            )

            db.add(user_role)

            customers = UserCustomer(
                user_id = registers.id,
                phone_number=payload.phone_number,
                address=payload.address,
                company_name=payload.company_name,
            )

            db.add(customers)

            #AuditLog saat berhasil register
            await AuditLogService.log(
                db,
                actor_type="USER",
                user_id=registers.id,
                event_type="ACTIVITY",
                action="REGISTER_USER",
                entity_type="USER",
                entity_id=registers.id,
                description=f"User {registers.username} registered",
            )

        get_access_token = create_access_token(str(registers.id))

        return RegisterResponse (
            access_token = get_access_token,
            token_type = "Bearer",
            username = registers.username,
        )

auth_service = AuthService()