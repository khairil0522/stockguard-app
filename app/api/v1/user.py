from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.auth import get_current_user,require_permission
from app.models.users import User
from app.schemas.user import UserCreate, UserUpdate, UserRead, UserDetailRead, UserRoleUpdate
from app.dependencies.auth import get_current_user
from app.services.user_service import (
    get_all_users,
    get_detail_user,
    create_user_one,
    update_user_one,
    update_user_role_one,
    remove_user,
)

from app.errors.auth import (
    EmailAlreadyUsedError,
    UsernameAlreadyUsedError,
    RoleNotFoundError,
    PermissionDeniedError,
    UserNotFoundError,
    RoleAlreadyAssignedError,
    RoleProtectedError
)

router = APIRouter(
    prefix="/users",
    tags=["User Management"],
)

@router.get(
    "/",
    response_model=list[UserRead],
    dependencies=[Depends(require_permission("user.read"))],
)
async def get_users(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await get_all_users(db, current_user.id)


@router.get(
    "/{user_id}",
    response_model=UserDetailRead,
    dependencies=[Depends(require_permission("user.read"))],
)
async def get_user_detail(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    return await get_detail_user(db, user_id)


@router.post(
    "/",
    response_model=UserDetailRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permission("user.create"))],
)
async def create_user(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return await create_user_one(
            db,
            payload,
            current_user,
        )

    except EmailAlreadyUsedError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail,
        )

    except UsernameAlreadyUsedError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail,
        )

    except RoleNotFoundError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail,
        )

    except PermissionDeniedError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail,
        )


@router.patch(
    "/{user_id}",
    response_model=UserDetailRead,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_permission("user.update"))],
)
async def update_user(
    user_id: UUID,
    payload: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return await update_user_one(
            db,
            payload,
            current_user,
            user_id,
        )

    except UserNotFoundError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail,
        )

    except EmailAlreadyUsedError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail,
        )

    except UsernameAlreadyUsedError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail,
        )


@router.patch(
    "/{user_id}/role",
    response_model=UserDetailRead,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_permission("user.assign"))],
)
async def update_user_role(
    user_id: UUID,
    payload: UserRoleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return await update_user_role_one(
            db,
            payload,
            current_user,
            user_id,
        )

    except UserNotFoundError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail,
        )

    except RoleNotFoundError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail,
        )

    except RoleAlreadyAssignedError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail,
        )

    except PermissionDeniedError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail,
        )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permission("user.status"))],
)
async def remove_user_endpoint(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    try:
        await remove_user(db, user_id)

    except UserNotFoundError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail,
        )

    except RoleProtectedError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail,
        )