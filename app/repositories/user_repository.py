from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.roles import Role
from app.models.user_roles import UserRole
from app.models.users import User


class UserRepository:

    async def get_by_id(self, db: AsyncSession, user_id: UUID) -> User | None:

        return await db.scalar(
            select(User).where(
                User.id == user_id
            )
        )

    async def get_by_id_for_update(self, db: AsyncSession, user_id: UUID) -> User | None:

        result = await db.execute(
            select(User)
            .where(User.id == user_id)
            .with_for_update()
        )

        return result.scalar_one_or_none()

    async def get_by_username(self, db: AsyncSession, username: str) -> User | None:

        return await db.scalar(
            select(User).where(
                User.username == username
            )
        )

    async def get_by_email(self, db: AsyncSession, email: str) -> User | None:

        return await db.scalar(
            select(User).where(
                User.email == email
            )
        )

    async def get_by_email_excluding_id(self, db: AsyncSession, email: str, user_id: UUID) -> User | None:

        return await db.scalar(
            select(User).where(
                User.email == email,
                User.id != user_id,
            )
        )

    async def get_by_username_excluding_id(self, db: AsyncSession, username: str, user_id: UUID) -> User | None:

        return await db.scalar(
            select(User).where(
                User.username == username,
                User.id != user_id,
            )
        )

    async def get_role_names(self, db: AsyncSession, user_id: UUID) -> list[str]:

        result = await db.scalars(
            select(Role.name)
            .join(
                UserRole,
                UserRole.role_id == Role.id,
            )
            .where(
                UserRole.user_id == user_id
            )
        )

        return result.all()

    async def get_user_role(self, db: AsyncSession, user_id: UUID) -> UserRole | None:

        return await db.scalar(
            select(UserRole).where(
                UserRole.user_id == user_id
            )
        )

    async def get_all_with_roles(self, db: AsyncSession, exclude_roles: list[str] | None = None) -> list[User]:

        statement = (
            select(User)
            .options(
                selectinload(User.user_roles)
            )
        )

        if exclude_roles:
            statement = (
                statement
                .join(UserRole, UserRole.user_id == User.id)
                .join(Role, Role.id == UserRole.role_id)
                .where(
                    Role.name.not_in(exclude_roles)
                )
            )

        result = await db.execute(statement)

        return result.scalars().unique().all()


user_repository = UserRepository()