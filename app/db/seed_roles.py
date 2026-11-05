import asyncio

from sqlalchemy import select

from app.db.session import AsyncSessionLocal
from app.models.role import Role


async def seed_roles():
    roles = [
        {
            "name": "ADMIN",
            "description": "System administrator",
            "is_system": True,
        },
        {
            "name": "STAFF",
            "description": "Internal staff user",
            "is_system": True,
        },
        {
            "name": "CUSTOMER",
            "description": "Customer user",
            "is_system": True,
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
    asyncio.run(seed_roles())