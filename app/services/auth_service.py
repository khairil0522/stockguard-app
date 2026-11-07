from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_password, create_access_token
from app.models.users import User
from app.errors.auth import InvalidUsernamePasswordError


async def login(db: AsyncSession, username: str, password: str):
    statement = select(User).where(User.username == username)

    user = await db.scalar(statement)

    if not user:
        raise InvalidUsernamePasswordError()

    if not verify_password(password, user.password_hash):
        raise InvalidUsernamePasswordError()

    return create_access_token(str(user.id))