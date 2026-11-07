import asyncio
import selectors

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.models.roles import Role
from app.models.permissions import Permission
from app.models.role_permissions import RolePermission


ROLE_PERMISSIONS = {
    "SUPERADMIN": "*",

    "ADMIN": [
        "product.read",
        "product.create",
        "product.update",
        "product.status",
        "inventory.read",
        "stock.adjust",
        "stock.history.read",
        "booking.read",
        "booking.create",
        "booking.update",
        "booking.confirm",
        "booking.cancel",
        "booking.complete",
        "user.read",
        "user.create",
        "user.update",
        "user.status",
        "user.role.assign",
        "role.read",
        "dashboard.read",
    ],

    "STAFF": [
        "product.read",
        "inventory.read",
        "stock.adjust",
        "stock.history.read",
        "booking.read",
        "booking.create",
        "booking.update",
        "booking.confirm",
        "booking.cancel",
        "booking.complete",
        "dashboard.read",
    ],

    "CUSTOMER": [
        "product.read",
        "booking.read",
        "booking.create",
        "booking.cancel",
    ],
}


async def seed_role_permissions():
    async with AsyncSessionLocal() as session:

        # Ambil seluruh permission yang tersedia di database.
        result = await session.execute(select(Permission))
        permissions = result.scalars().all()

        permission_by_code = {
            permission.code: permission
            for permission in permissions
        }

        for role_name, permission_codes in ROLE_PERMISSIONS.items():

            # Cari role berdasarkan nama.
            role_result = await session.execute(
                select(Role).where(Role.name == role_name)
            )
            role = role_result.scalar_one_or_none()

            if not role:
                print(f"Role {role_name} tidak ditemukan.")
                continue

            # SUPER_ADMIN mendapatkan seluruh permission.
            if permission_codes == "*":
                codes = permission_by_code.keys()
            else:
                codes = permission_codes

            for code in codes:

                permission = permission_by_code.get(code)

                if not permission:
                    print(f"Permission {code} tidak ditemukan.")
                    continue

                # Cek apakah relasi sudah ada.
                existing = await session.execute(
                    select(RolePermission).where(
                        RolePermission.role_id == role.id,
                        RolePermission.permission_id == permission.id,
                    )
                )

                if existing.scalar_one_or_none():
                    continue

                # Tambahkan relasi Role -> Permission.
                session.add(
                    RolePermission(
                        role_id=role.id,
                        permission_id=permission.id,
                    )
                )

        await session.commit()


if __name__ == "__main__":
    asyncio.run(
        seed_role_permissions(),
        loop_factory=lambda: asyncio.SelectorEventLoop(
            selectors.SelectSelector()
        ),
    )