from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.audit.rbac_audit import RBACAudit
from app.errors.auth import PermissionNotFoundError
from app.models.role_permissions import RolePermission
from app.models.users import User
from app.repositories.permission_repository import permission_repository
from app.repositories.role_permission_repository import role_permission_repository
from app.schemas.role_permission import (
    RolePermissionAssign,
    RolePermissionRead,
    RolePermissionRemove,
)


class RolePermissionService:
    async def get_permissions_by_role(self, db: AsyncSession, role_id: UUID) -> list[RolePermissionRead]:
        rows = await role_permission_repository.get_permissions_by_role(db, role_id)

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

    async def assign_permissions_to_role(self, db: AsyncSession, role_id: UUID, payload: RolePermissionAssign, current_user: User) -> list[RolePermissionRead]:

        # 1. Cek permission yang dikirim memang ada di master Permission
        permissions = await permission_repository.get_by_ids(db, payload.permission_ids)

        # Pastikan semua permission yang diminta memang tersedia
        if len(permissions) != len(set(payload.permission_ids)):
            raise PermissionNotFoundError()

        # 2. Cek permission yang sudah dimiliki oleh role ini
        existing_role_permissions = await role_permission_repository.get_by_role_and_permission_ids(db, role_id, payload.permission_ids)

        # Ambil ID permission yang sudah ada
        existing_permission_ids = {
            role_permission.permission_id
            for role_permission in existing_role_permissions
        }

        # 3. Cari permission yang belum dimiliki role
        permission_ids_to_add = (
            set(payload.permission_ids) - existing_permission_ids
        )

        before = {
            "permission_ids": [
                str(permission_id)
                for permission_id in existing_permission_ids
            ],
        }

        after = {
            "permission_ids": [
                str(permission_id)
                for permission_id in (
                    existing_permission_ids | permission_ids_to_add
                )
            ],
        }

        # 4. Tambahkan association yang baru
        for permission_id in permission_ids_to_add:

            role_permission = RolePermission(
                role_id=role_id,
                permission_id=permission_id,
            )

            db.add(role_permission)

        rbac_audit = RBACAudit(
            db=db,
            actor_id=current_user,
            target_id=role_id,
            target_type="ROLE",
        )

        await rbac_audit.grant_permission(
            permission_name="ROLE_PERMISSIONS",
            before=before,
            after=after,
        )

        await db.commit()

        # 5. Ambil ulang association untuk response lewat fungsi get_permissions_by_role
        return await self.get_permissions_by_role(db, role_id)

    async def remove_permissions_from_role(self, db: AsyncSession, role_id: UUID, payload: RolePermissionRemove, current_user: User) -> list[RolePermissionRead]:
        # Ambil dari permission yang dikirim
        permissions = await role_permission_repository.get_by_role_and_permission_ids(db, role_id, payload.permission_ids)

        existing_permission_ids = {
            role_permission.permission_id
            for role_permission in permissions
        }

        before = {
            "permission_ids": [
                str(permission_id)
                for permission_id in existing_permission_ids
            ],
        }

        after = {
            "permission_ids": [],
        }

        for delete in permissions:
            await db.delete(delete)

        rbac_audit = RBACAudit(
            db=db,
            actor_id=current_user.id,
            target_id=role_id,
            target_type="ROLE",
        )

        await rbac_audit.revoke_permission(
            permission_name="ROLE_PERMISSIONS",
            before=before,
            after=after,
        )

        await db.commit()

        return await self.get_permissions_by_role(db, role_id)

rolepermission_service = RolePermissionService()