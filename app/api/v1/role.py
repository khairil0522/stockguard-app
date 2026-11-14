from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.auth import get_current_user, get_current_user_roles, get_current_user_permissions, require_permission
from app.errors.auth import RoleAlreadyError

from app.db.session import get_db
from app.schemas.role import RoleRead, RoleCreate, RoleUpdate
from app.services.role_service import role_service

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.get(
    "/",
    response_model=list[RoleRead],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_permission("role.read"))],
)
async def get_roles(db: AsyncSession = Depends(get_db)):
    return await role_service.get_all(db)

@router.post(
    "/",
    response_model=RoleRead,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_permission("role.create"))],
)
async def create_role(payload: RoleCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await role_service.create(db, payload)
    except RoleAlreadyError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail = exc.detail
        )


@router.patch(
    "/{role_id}",
    response_model=RoleRead,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_permission("role.update"))],
)
async def update_role(
    role_id: UUID,
    payload: RoleUpdate,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await role_service.update(db, payload, role_id)

    except RoleAlreadyError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail,
        )

@router.patch(
    "/{role_id}/status",
    response_model=RoleRead,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_permission("role.update"))],
)
async def update_status_role(
    role_id: UUID,
    is_active: bool,
    db: AsyncSession = Depends(get_db),
):
    return await role_service.restatus(db, role_id, is_active)