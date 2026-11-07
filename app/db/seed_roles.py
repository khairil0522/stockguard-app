import asyncio
import selectors

from sqlalchemy import select

from app.db.session import AsyncSessionLocal
from app.models.roles import Role


async def seed_roles():
    roles = [
        {
            "name": "SUPERADMIN",
            "description": "System Control",
            "is_system": True,
            "is_active": True
        },        
        {
            "name": "ADMIN",
            "description": "System administrator",
            "is_system": True,
            "is_active": True
        },
        {
            "name": "STAFF",
            "description": "Internal staff user",
            "is_system": True,
            "is_active": True
        },
        {
            "name": "CUSTOMER",
            "description": "Customer user",
            "is_system": True,
            "is_active": True
        },
    ]

    async with AsyncSessionLocal() as session:
        for role_data in roles:
            result = await session.execute(
                select(Role).where(Role.name == role_data["name"])
            )

            existing_role = result.scalar_one_or_none()

            if existing_role:
                continue

            session.add(Role(**role_data))

        await session.commit()


if __name__ == "__main__":
    asyncio.run(
        seed_roles(),
        loop_factory=lambda: asyncio.SelectorEventLoop(
            selectors.SelectSelector()
        ),
    )