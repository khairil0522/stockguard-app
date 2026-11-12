from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.role_permission import (
    RolePermissionAssign,
    RolePermissionRemove,
    RolePermissionRead,
)
from app.services.role_permission_service import (
    get_permissions_by_role,
    assign_permissions_to_role,
    remove_permissions_from_role,
)
from app.errors.auth import (
    PermissionNotFoundError,
)

from app.dependencies.auth import require_permission

router = APIRouter(prefix="/roles", tags=["RolePermissions"])

@router.get(
    "/{role_id}/permissions",
    response_model=list[RolePermissionRead],
    dependencies=[Depends(require_permission("permission.manage"))],
    status_code=status.HTTP_200_OK,
)
async def get_role_permissions(
    role_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await get_permissions_by_role(db, role_id)

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )

@router.post(
    "/{role_id}/permissions",
    response_model=list[RolePermissionRead],
    dependencies=[Depends(require_permission("permission.manage"))],
    status_code=status.HTTP_200_OK,
)
async def assign_role_permissions(
    role_id: UUID,
    payload: RolePermissionAssign,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await assign_permissions_to_role(
            db,
            role_id,
            payload,
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
    db: AsyncSession = Depends(get_db),
):
    try:
        return await remove_permissions_from_role(
            db,
            role_id,
            payload,
        )

    except PermissionNotFoundError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail,
        )