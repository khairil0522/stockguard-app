from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.auth import require_permission
from app.errors.auth import PermissionAlreadyError
from app.db.session import get_db
from app.schemas.permission import (
    PermissionRead,
    PermissionCreate,
    PermissionUpdate,
)
from app.services.permission_service import (
    get_all_permissions,
    get_permission_by_id,
    create_permissions,
    update_permissions,
)


router = APIRouter(
    prefix="/permissions",
    tags=["Permissions"],
)


@router.get(
    "/",
    response_model=list[PermissionRead],
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(require_permission("permission.read"))
    ],
)
async def get_permissions(
    db: AsyncSession = Depends(get_db),
):
    return await get_all_permissions(db)


@router.get(
    "/{permission_id}",
    response_model=PermissionRead,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(require_permission("permission.read"))
    ],
)
async def get_permission(
    permission_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    return await get_permission_by_id(
        db,
        permission_id,
    )


@router.post(
    "/",
    response_model=PermissionRead,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(require_permission("permission.manage"))
    ],
)
async def create_permission(
    payload: PermissionCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await create_permissions(
            db,
            payload,
        )

    except PermissionAlreadyError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail,
        )


@router.patch(
    "/{permission_id}",
    response_model=PermissionRead,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(require_permission("permission.manage"))
    ],
)
async def update_permission(
    permission_id: UUID,
    payload: PermissionUpdate,
    db: AsyncSession = Depends(get_db),
):
    return await update_permissions(
        db,
        permission_id,
        payload,
    )