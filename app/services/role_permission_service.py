from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.errors.auth import PermissionNotFoundError
from app.models.roles import Role
from app.models.role_permissions import RolePermission
from app.models.permissions import Permission
from app.schemas.role_permission import RolePermissionAssign, RolePermissionRemove, RolePermissionRead

async def get_permissions_by_role(db: AsyncSession, role_id: UUID) -> list[RolePermissionRead]:
    result = await db.execute(
        select(Permission, RolePermission)
        .outerjoin(RolePermission,
            (RolePermission.permission_id == Permission.id)
            & (RolePermission.role_id == role_id),
        )
    )

    rows = result.all()

    permission_list = []

    for permission, role_permission in rows:
        permission_list.append(
            RolePermissionRead(
                permission_id=permission.id,
                permission_code=permission.code,
                assigned=role_permission is not None,
            )
        )

    return permission_list

async def assign_permissions_to_role(db: AsyncSession, role_id: UUID, payload: RolePermissionAssign) -> list[RolePermissionRead]:

    # 1. Cek permission yang dikirim memang ada di master Permission
    result = await db.execute(
        select(Permission).where(
            Permission.id.in_(payload.permission_ids)
        )
    )

    permissions = result.scalars().all()

    # Pastikan semua permission yang diminta memang tersedia
    if len(permissions) != len(set(payload.permission_ids)):
        raise PermissionNotFoundError()

    # 2. Cek permission yang sudah dimiliki oleh role ini
    result = await db.execute(
        select(RolePermission).where(
            RolePermission.role_id == role_id,
            RolePermission.permission_id.in_(payload.permission_ids),
        )
    )

    existing_role_permissions = result.scalars().all()

    # Ambil ID permission yang sudah ada
    existing_permission_ids = {
        role_permission.permission_id
        for role_permission in existing_role_permissions
    }

    # 3. Cari permission yang belum dimiliki role
    permission_ids_to_add = (
        set(payload.permission_ids) - existing_permission_ids
    )

    # 4. Tambahkan association yang baru
    for permission_id in permission_ids_to_add:
        role_permission = RolePermission(
            role_id=role_id,
            permission_id=permission_id,
        )

        db.add(role_permission)

    await db.commit()

    # 5. Ambil ulang association untuk response lewat fungsi get_permissions_by_role
    return await get_permissions_by_role(db, role_id)

async def remove_permissions_from_role(db: AsyncSession, role_id: UUID, payload: RolePermissionRemove) -> list[RolePermissionRead]:
    # Ambil dari permission yang dikirim
    result = await db.execute(
        select(RolePermission).where(
            RolePermission.permission_id.in_(payload.permission_ids),
            RolePermission.role_id == role_id,
        )
    )

    permissions = result.scalars().all()

    for delete in permissions:
        await db.delete(delete)

    await db.commit()

    return await get_permissions_by_role(db, role_id)
