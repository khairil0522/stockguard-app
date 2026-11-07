import asyncio
import selectors

from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.models.permissions import Permission


async def seed_permissions():
    permissions = [
        {
            "code": "role.read",
            "name": "Read Role",
            "description": "Melihat data role",
        },
        {
            "code": "role.create",
            "name": "Create Role",
            "description": "Membuat role baru",
        },
        {
            "code": "role.update",
            "name": "Update Role",
            "description": "Mengubah data role",
        },
        {
            "code": "role.status",
            "name": "Manage Role Status",
            "description": "Mengaktifkan atau menonaktifkan role",
        },
        {
            "code": "permission.read",
            "name": "Read Permission",
            "description": "Melihat data permission",
        },
        {
            "code": "permission.manage",
            "name": "Manage Permission",
            "description": "Mengelola permission sistem",
        },
        {
            "code": "user.role.assign",
            "name": "Assign User Role",
            "description": "Memberikan role kepada user",
        },
        {
            "code": "product.read",
            "name": "Read Product",
            "description": "Melihat daftar dan detail produk",
        },
        {
            "code": "product.create",
            "name": "Create Product",
            "description": "Membuat produk baru",
        },
        {
            "code": "product.update",
            "name": "Update Product",
            "description": "Mengubah data produk",
        },
        {
            "code": "product.status",
            "name": "Manage Product Status",
            "description": "Mengaktifkan atau menonaktifkan produk",
        },
        {
            "code": "inventory.read",
            "name": "Read Inventory",
            "description": "Melihat data inventory",
        },
        {
            "code": "stock.adjust",
            "name": "Adjust Stock",
            "description": "Menambah atau mengurangi stok",
        },
        {
            "code": "stock.history.read",
            "name": "Read Stock History",
            "description": "Melihat riwayat perubahan stok",
        },
        {
            "code": "booking.read",
            "name": "Read Booking",
            "description": "Melihat data booking",
        },
        {
            "code": "booking.create",
            "name": "Create Booking",
            "description": "Membuat booking",
        },
        {
            "code": "booking.update",
            "name": "Update Booking",
            "description": "Mengubah data booking",
        },
        {
            "code": "booking.confirm",
            "name": "Confirm Booking",
            "description": "Mengonfirmasi booking",
        },
        {
            "code": "booking.cancel",
            "name": "Cancel Booking",
            "description": "Membatalkan booking",
        },
        {
            "code": "booking.complete",
            "name": "Complete Booking",
            "description": "Menyelesaikan booking",
        },
        {
            "code": "user.read",
            "name": "Read User",
            "description": "Melihat data user",
        },
        {
            "code": "user.create",
            "name": "Create User",
            "description": "Membuat user",
        },
        {
            "code": "user.update",
            "name": "Update User",
            "description": "Mengubah data user",
        },
        {
            "code": "user.status",
            "name": "Manage User Status",
            "description": "Mengaktifkan atau menonaktifkan user",
        },
        {
            "code": "role.read",
            "name": "Read Role",
            "description": "Melihat data role",
        },
        {
            "code": "role.manage",
            "name": "Manage Role",
            "description": "Mengatur role dan assignment",
        },
        {
            "code": "permission.read",
            "name": "Read Permission",
            "description": "Melihat data permission",
        },
        {
            "code": "dashboard.read",
            "name": "Read Dashboard",
            "description": "Melihat dashboard",
        },
    ]

    async with AsyncSessionLocal() as session:
        for permission_data in permissions:
            result = await session.execute(
                select(Permission).where(
                    Permission.code == permission_data["code"]
                )
            )

            existing_permission = result.scalar_one_or_none()

            if existing_permission:
                continue

            session.add(Permission(**permission_data))

        await session.commit()


if __name__ == "__main__":
    asyncio.run(
        seed_permissions(),
        loop_factory=lambda: asyncio.SelectorEventLoop(
            selectors.SelectSelector()
        ),
    )