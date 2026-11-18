from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.auth import require_permission
from app.errors.auth import PermissionAlreadyError, PermissionNotFoundError
from app.schemas.permission import (
    PermissionCreate,
    PermissionRead,
    PermissionUpdate,
)
from app.services.permission_service import permission_service

router = APIRouter(
    prefix="/permissions",
    tags=["Permissions"],
)

DEPENDENCY_DB = Depends(get_db)


@router.get(
    "/",
    response_model=list[PermissionRead],
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(require_permission("permission.read"))
    ],
)
async def get_permissions(
    db: AsyncSession = DEPENDENCY_DB,
):
    return await permission_service.get_all(db)


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
    db: AsyncSession = DEPENDENCY_DB,
):
    try:
        return await permission_service.get_by_id(
        db,
        permission_id,
        )

    except PermissionNotFoundError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail,
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
    db: AsyncSession = DEPENDENCY_DB,
):
    try:
        return await permission_service.create(
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
    db: AsyncSession = DEPENDENCY_DB,
):
    try:
        return await permission_service.update(
            db,
            permission_id,
            payload,
        )

    except PermissionNotFoundError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail,
        )