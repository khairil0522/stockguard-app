from uuid import UUID

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.users import User
from app.models.roles import Role
from app.models.user_roles import UserRole
from app.models.role_permissions import RolePermission

from app.errors.auth import PermissionDeniedError

from sqlalchemy.orm import selectinload

bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:

    try:
        user_id = decode_access_token(credentials.credentials)

    except (jwt.InvalidTokenError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak valid atau sudah kedaluwarsa.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak valid.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await db.scalar(
        select(User).where(User.id == user_uuid)
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User tidak ditemukan.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User tidak aktif.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user

async def get_current_user_roles(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    statement = (
        select(User)
        .where(User.id == current_user.id)
        .options(
            selectinload(User.user_roles).selectinload(UserRole.role)
        )
    )

    user = await db.scalar(statement)

    return [user_role.role for user_role in user.user_roles]

async def get_current_user_permissions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    statement = (
        select(User)
        .where(User.id == current_user.id)
        .options(
            selectinload(User.user_roles)
            .selectinload(UserRole.role)
            .selectinload(Role.role_permissions)
            .selectinload(RolePermission.permission)
        )
    )

    user = await db.scalar(statement)

    permissions = set()

    for user_role in user.user_roles:
        for role_permission in user_role.role.role_permissions:
            permissions.add(role_permission.permission.code)

    return permissions

def require_permission(required_permission: str):

    async def permission_checker(
        permissions=Depends(get_current_user_permissions),
    ):
        if "*" in permissions:
            return

        if required_permission not in permissions:
            raise PermissionDeniedError()

    return permission_checker