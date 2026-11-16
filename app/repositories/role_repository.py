from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.roles import Role


class RoleRepository:

    async def get_all(self, db: AsyncSession,) -> list[Role]:

        result = await db.execute(
            select(Role)
        )

        return result.scalars().all()

    async def get_by_id(self, db: AsyncSession, role_id: UUID) -> Role | None:

        return await db.scalar(
            select(Role).where(
                Role.id == role_id
            )
        )

    async def get_by_name(self, db: AsyncSession, name: str) -> Role | None:

        return await db.scalar(
            select(Role).where(
                Role.name == name
            )
        )

    async def get_by_name_excluding_id(self, db: AsyncSession, name: str, role_id: UUID) -> Role | None:

        return await db.scalar(
            select(Role).where(
                Role.name == name,
                Role.id != role_id,
            )
        )


role_repository = RoleRepository()