import asyncio
import selectors

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.db.session import AsyncSessionLocal
from app.models.users import User
from app.models.roles import Role
from app.models.user_roles import UserRole


async def seed_super_admin():
    async with AsyncSessionLocal() as session:

        # Cari role SUPER_ADMIN yang sudah dibuat sebelumnya.
        role_result = await session.execute(
            select(Role).where(Role.name == "SUPERADMIN")
        )
        super_admin_role = role_result.scalar_one_or_none()

        if not super_admin_role:
            print("Role SUPER_ADMIN belum ditemukan.")
            return

        # Cek apakah username sudah digunakan.
        user_result = await session.execute(
            select(User).where(User.username == "superadmin")
        )
        existing_user = user_result.scalar_one_or_none()

        if existing_user:
            print("User superadmin sudah ada.")
            return

        # Buat user bootstrap pertama.
        user = User(
            username="superadmin",
            email="admin@stockguard.local",
            full_name="StockGuard Super Admin",
            password_hash=hash_password("SuperAdmin123!"),
            is_active=True,
        )

        session.add(user)

        # Flush diperlukan agar user.id tersedia
        # sebelum membuat relasi UserRole.
        await session.flush()

        session.add(
            UserRole(
                user_id=user.id,
                role_id=super_admin_role.id,
            )
        )

        await session.commit()

        print("SUPER_ADMIN berhasil dibuat.")


if __name__ == "__main__":
    asyncio.run(
        seed_super_admin(),
        loop_factory=lambda: asyncio.SelectorEventLoop(
            selectors.SelectSelector()
        ),
    )