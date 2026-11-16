from uuid import UUID

from app.repositories.role_repository import role_repository
from sqlalchemy.ext.asyncio import AsyncSession

from app.errors.auth import (
    ProtectedRoleError,
    RoleAlreadyError,
    RoleNotFoundError,
)
from app.models.roles import Role
from app.schemas.role import RoleCreate, RoleRead, RoleUpdate

class RoleService:
    async def get_all(self, db: AsyncSession) -> list[RoleRead]:
        get_roles = await role_repository.get_all(db)

        if not get_roles:
            return []

        return get_roles


    async def get_by_id(self, db: AsyncSession, role_id: UUID) -> RoleRead:
        get_role = await role_repository.get_by_id(db, role_id)

        if not get_role:
            raise RoleNotFoundError()

        return get_role


    async def create(self, db: AsyncSession, payload: RoleCreate) -> RoleRead:

        existing_role = await role_repository.get_by_name(db, payload.name)

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


    async def update(self, db: AsyncSession, payload: RoleUpdate, role_id: UUID) -> RoleRead:

        role = await role_repository.get_by_id(db, role_id)

        if not role:
            raise RoleNotFoundError()

        existing_role = await role_repository.get_by_name_excluding_id(db, payload.name, role_id)

        if existing_role:
            raise RoleAlreadyError()

        role.name = payload.name
        role.description = payload.description

        await db.commit()
        await db.refresh(role)

        return RoleRead.model_validate(role)


    async def restatus(self, db: AsyncSession, role_id: UUID, is_active: bool) -> RoleRead:

        role = await role_repository.get_by_id(db, role_id)

        if role is None:
            raise RoleNotFoundError()

        if role.is_system:
            raise ProtectedRoleError()

        role.is_active = is_active

        await db.commit()
        await db.refresh(role)

        return role

role_service = RoleService()