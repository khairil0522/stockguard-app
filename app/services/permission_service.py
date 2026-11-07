from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.errors.auth import (PermissionAlreadyError, PermissionNotFoundError)
from app.models.permissions import Permission
from app.schemas.permission import (PermissionCreate,PermissionRead,PermissionUpdate)


async def get_all_permissions(db: AsyncSession) -> list[PermissionRead]:
    result = await db.execute(
        select(Permission)
    )

    permissions = result.scalars().all()

    return permissions


async def get_permission_by_id(
    db: AsyncSession,
    permission_id: UUID,
) -> PermissionRead:

    permission = await db.scalar(
        select(Permission).where(
            Permission.id == permission_id
        )
    )

    if not permission:
        raise PermissionNotFoundError()

    return permission


async def create_permissions(
    db: AsyncSession,
    payload: PermissionCreate,
) -> PermissionRead:

    existing_permission = await db.scalar(
        select(Permission).where(
            Permission.code == payload.code
        )
    )

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


async def update_permissions(
    db: AsyncSession,
    permission_id: UUID,
    payload: PermissionUpdate,
) -> PermissionRead:

    permission = await db.scalar(
        select(Permission).where(
            Permission.id == permission_id
        )
    )

    if not permission:
        raise PermissionNotFoundError()

    permission.name = payload.name
    permission.description = payload.description

    await db.commit()
    await db.refresh(permission)

    return PermissionRead.model_validate(permission)