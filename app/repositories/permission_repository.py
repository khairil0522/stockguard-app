from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.permissions import Permission


class PermissionRepository:

    async def get_all(self, db: AsyncSession) -> list[Permission]:

        result = await db.execute(
            select(Permission)
        )

        return result.scalars().all()


    async def get_by_id(self, db: AsyncSession, permission_id: UUID) -> Permission | None:

        return await db.scalar(
            select(Permission).where(
                Permission.id == permission_id
            )
        )


    async def get_by_code(self, db: AsyncSession, code: str) -> Permission | None:

        return await db.scalar(
            select(Permission).where(
                Permission.code == code
            )
        )


    async def get_by_ids(self, db: AsyncSession, permission_ids: list[UUID]) -> list[Permission]:

        result = await db.execute(
            select(Permission).where(
                Permission.id.in_(permission_ids)
            )
        )

        return result.scalars().all()


permission_repository = PermissionRepository()