from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.auth import get_current_user, get_current_user_roles, get_current_user_permissions

from app.db.session import get_db
from app.schemas.auth import LoginRequest, LoginResponse, UserMeResponse, RegisterResponse, RegisterRequest
from app.models.users import User
from app.services.auth_service import auth_service
from app.errors.auth import InvalidUsernamePasswordError, UsernameAlreadyUsedError, EmailAlreadyUsedError, RoleNotFoundError


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=RegisterResponse)
async def register_user(
    payload: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await auth_service.register(db, payload)
    
    except UsernameAlreadyUsedError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail,
        )

    except EmailAlreadyUsedError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail,
        )

    except RoleNotFoundError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail,
        ) 


@router.post("/login", response_model=LoginResponse)
async def login_user(
    payload: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        access_token = await auth_service.login(
        db,
        payload.username,
        payload.password,
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }
    except InvalidUsernamePasswordError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail
        )

@router.get("/me", response_model=UserMeResponse)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    return {
        "id": str(current_user.id),
        "username": current_user.username,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "is_active": current_user.is_active,
    }

@router.get("/roles")
async def get_my_roles(
    roles = Depends(get_current_user_roles),
):
    return [
        {
            "id": str(role.id),
            "name": role.name,
        }
        for role in roles
    ]

@router.get("/permissions")
async def get_my_permissions(
    permissions = Depends(get_current_user_permissions),
):
    return {
        "permissions": sorted(permissions)
    }