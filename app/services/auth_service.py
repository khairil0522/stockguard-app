from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_password, create_access_token, hash_password
from app.models.users import User
from app.models.roles import Role
from app.models.user_customers import UserCustomer
from app.models.user_roles import UserRole
from app.errors.auth import InvalidUsernamePasswordError, UsernameAlreadyUsedError, EmailAlreadyUsedError, RoleNotFoundError
from app.schemas.auth import RegisterRequest, RegisterResponse

from app.audit.auth_audit import AuthAudit

class AuthService:
    async def login(self, db: AsyncSession, username: str, password: str):
        statement = select(User).where(User.username == username)
        user = await db.scalar(statement)

        if not user:
            auth_audit = AuthAudit(db)

            await auth_audit.login_failed_system(
                username=username,
            )

            await db.commit()
            raise InvalidUsernamePasswordError()

        if not verify_password(password, user.password_hash):
            auth_audit = AuthAudit(db)

            await auth_audit.login_failed_user(
                user_id=user.id,
                username=username,
            )

            await db.commit()
            raise InvalidUsernamePasswordError()

        access_token = create_access_token(str(user.id))

        auth_audit = AuthAudit(db)

        await auth_audit.login_success(
            user_id=user.id,
            username=user.username,
        )

        await db.commit()

        return access_token

    async def register(self, db: AsyncSession, payload: RegisterRequest) -> RegisterResponse:

        existing_username = await db.scalar(
            select(User).where(User.username == payload.username)
        )

        if existing_username:
            auth_audit = AuthAudit(db)

            await auth_audit.register_failed(
                username=payload.username,
                reason="USERNAME_ALREADY_USED",
            )

            await db.commit()

            raise UsernameAlreadyUsedError()

        existing_email = await db.scalar(
            select(User).where(User.email == payload.email)
        )

        if existing_email:
            auth_audit = AuthAudit(db)

            await auth_audit.register_failed(
                username=payload.username,
                reason="EMAIL_ALREADY_USED",
            )

            await db.commit()

            raise EmailAlreadyUsedError()

        async with db.begin():
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
                user_id=registers.id,
                role_id=get_role_id
            )

            db.add(user_role)

            customers = UserCustomer(
                user_id=registers.id,
                phone_number=payload.phone_number,
                address=payload.address,
                company_name=payload.company_name,
            )

            db.add(customers)

            auth_audit = AuthAudit(db)

            await auth_audit.register(
                user_id=registers.id,
                username=registers.username,
            )

        get_access_token = create_access_token(str(registers.id))

        return RegisterResponse(
            access_token=get_access_token,
            token_type="Bearer",
            username=registers.username,
        )

auth_service = AuthService()