from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.auth import get_current_user, require_permission
from app.errors.auth import PermissionNotFoundError
from app.models.users import User
from app.schemas.role_permission import (
    RolePermissionAssign,
    RolePermissionRead,
    RolePermissionRemove,
)
from app.services.role_permission_service import rolepermission_service

router = APIRouter(prefix="/roles", tags=["RolePermissions"])
DB_DEPENDENCY = Depends(get_db)


@router.get(
    "/{role_id}/permissions",
    response_model=list[RolePermissionRead],
    dependencies=[Depends(require_permission("permission.manage"))],
    status_code=status.HTTP_200_OK,
)
async def get_role_permissions(
    role_id: UUID,
    db: AsyncSession = DB_DEPENDENCY,
):
    return await rolepermission_service.get_permissions_by_role(db, role_id)


@router.post(
    "/{role_id}/permissions",
    response_model=list[RolePermissionRead],
    dependencies=[Depends(require_permission("permission.manage"))],
    status_code=status.HTTP_200_OK,
)
async def assign_role_permissions(
    role_id: UUID,
    payload: RolePermissionAssign,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = DB_DEPENDENCY,
):
    try:
        return await rolepermission_service.assign_permissions_to_role(
            db,
            role_id,
            payload,
            current_user.id,
        )

    except PermissionNotFoundError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail,
        )

@router.delete(
    "/{role_id}/permissions",
    response_model=list[RolePermissionRead],
    dependencies=[Depends(require_permission("permission.manage"))],
    status_code=status.HTTP_200_OK,
)
async def remove_role_permissions(
    role_id: UUID,
    payload: RolePermissionRemove,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = DB_DEPENDENCY,
):
    try:
        return await rolepermission_service.remove_permissions_from_role(
            db,
            role_id,
            payload,
            current_user,
        )

    except PermissionNotFoundError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail,
        )