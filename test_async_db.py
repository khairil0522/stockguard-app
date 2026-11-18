import asyncio
import selectors

from sqlalchemy import text

from app.db.session import AsyncSessionLocal


async def test_connection():
    async with AsyncSessionLocal() as db:
        result = await db.execute(text("SELECT 1"))
        print(result.scalar())


if __name__ == "__main__":
    asyncio.run(
        test_connection(),
        loop_factory=lambda: asyncio.SelectorEventLoop(
            selectors.SelectSelector()
        ),
    )