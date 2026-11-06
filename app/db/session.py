from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

engine = create_async_engine(
    settings.database_url,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as db:
        yield db


# ini merupakan sync bisa jadi dokumentasi untuk belajar
# from collections.abc import Generator

# from sqlalchemy import create_engine
# from sqlalchemy.orm import Session, sessionmaker

# from app.core.config import settings


# engine = create_engine(
#     settings.database_url,
#     pool_pre_ping=True,
# )

# SessionLocal = sessionmaker(
#     bind=engine,
#     class_=Session,
#     autoflush=False,
#     expire_on_commit=False,
# )


# def get_db() -> Generator[Session, None, None]:
#     db = SessionLocal()

#     try:
#         yield db
#     finally:
#         db.close()