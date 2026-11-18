from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.errors.auth import PermissionAlreadyError, PermissionNotFoundError
from app.models.permissions import Permission
from app.repositories.permission_repository import permission_repository
from app.schemas.permission import PermissionCreate, PermissionRead, PermissionUpdate


class PermissionService:

    async def get_all(self, db: AsyncSession) -> list[PermissionRead]:

        permissions = await permission_repository.get_all(db)
        
        return [
            PermissionRead.model_validate(permission)
            for permission in permissions
        ]


    async def get_by_id(self, db: AsyncSession, permission_id: UUID) -> PermissionRead:

        permission = await permission_repository.get_by_id(db, permission_id)

        if not permission:
            raise PermissionNotFoundError()

        return permission


    async def create(self, db: AsyncSession, payload: PermissionCreate) -> PermissionRead:

        existing_permission = await permission_repository.get_by_code(db, payload.code)

        if existing_permission:
            raise PermissionAlreadyError()

        permission = Permission(
            code=payload.code,
            name=payload.name,
            description=payload.description,
        )

        db.add(permission)
        await db.commit()
        await db.refresh(permission)

        return PermissionRead.model_validate(permission)


    async def update(self, db: AsyncSession, permission_id: UUID, payload: PermissionUpdate) -> PermissionRead:

        permission = await permission_repository.get_by_id(db, permission_id)

        if not permission:
            raise PermissionNotFoundError()

        permission.name = payload.name
        permission.description = payload.description

        await db.commit()
        await db.refresh(permission)

        return PermissionRead.model_validate(permission)

permission_service = PermissionService()