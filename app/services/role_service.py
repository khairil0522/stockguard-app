from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.errors.auth import (
    ProtectedRoleError,
    RoleAlreadyError,
    RoleNotFoundError,
)
from app.models.roles import Role
from app.schemas.role import RoleCreate, RoleRead, RoleUpdate


async def get_all_roles(
    db: AsyncSession,
) -> list[RoleRead]:
    result = await db.execute(
        select(Role)
    )

    get_roles = result.scalars().all()

    if not get_roles:
        return []

    return get_roles


async def get_role_by_id(
    db: AsyncSession,
    role_id: UUID,
) -> RoleRead:
    get_role = await db.scalar(
        select(Role).where(Role.id == role_id)
    )

    if not get_role:
        raise RoleNotFoundError()

    return get_role


async def create_roles(
    db: AsyncSession,
    payload: RoleCreate,
) -> RoleRead:

    existing_role = await db.scalar(
        select(Role).where(Role.name == payload.name)
    )

    if existing_role:
        raise RoleAlreadyError()

    role = Role(
        name=payload.name,
        description=payload.description,
        is_active=True,
        is_system=False,
    )

    db.add(role)

    await db.commit()
    await db.refresh(role)

    return RoleRead.model_validate(role)


async def update_roles(
    db: AsyncSession,
    payload: RoleUpdate,
    role_id: UUID,
) -> RoleRead:

    role = await db.scalar(
        select(Role).where(Role.id == role_id)
    )

    if not role:
        raise RoleNotFoundError()

    existing_role = await db.scalar(
        select(Role).where(
            Role.name == payload.name,
            Role.id != role_id,
        )
    )

    if existing_role:
        raise RoleAlreadyError()

    role.name = payload.name
    role.description = payload.description

    await db.commit()
    await db.refresh(role)

    return RoleRead.model_validate(role)    


async def restatus_role(
    db: AsyncSession,
    role_id: UUID,
    is_active: bool,
) -> RoleRead:

    role = await db.get(Role, role_id)

    if role is None:
        raise RoleNotFoundError()

    if role.is_system:
        raise ProtectedRoleError()

    role.is_active = is_active

    await db.commit()
    await db.refresh(role)

    return role