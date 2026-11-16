from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.permissions import Permission
from app.models.role_permissions import RolePermission


class RolePermissionRepository:

    async def get_by_role_and_permission_ids(self, db: AsyncSession, role_id: UUID, permission_ids: list[UUID]) -> list[RolePermission]:

        result = await db.execute(
            select(RolePermission).where(
                RolePermission.role_id == role_id,
                RolePermission.permission_id.in_(permission_ids),
            )
        )

        return result.scalars().all()


    async def get_permissions_by_role(self, db: AsyncSession, role_id: UUID):

        result = await db.execute(
            select(Permission, RolePermission)
            .outerjoin(
                RolePermission,
                (RolePermission.permission_id == Permission.id)
                & (RolePermission.role_id == role_id),
            )
        )

        return result.all()


role_permission_repository = RolePermissionRepository()