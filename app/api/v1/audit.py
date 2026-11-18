from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.auth import get_current_user, require_permission
from app.errors.auth import LogNotFoundError, PermissionDeniedError
from app.models.users import User
from app.schemas.audit import AuditLogDetailResponse, AuditLogResponse
from app.services.audit_log_service import AuditLogService

router = APIRouter(
    prefix="/log",
    tags=["Audit Log"],
)

DB_SESSION_DEPENDENCY = Depends(get_db)
CURRENT_USER_DEPENDENCY = Depends(get_current_user)

@router.get("/show",response_model=AuditLogResponse, 
            dependencies=[Depends(require_permission("auditlog.read"))],)
async def audit_log(db: AsyncSession = DB_SESSION_DEPENDENCY):
    return await AuditLogService.show(db)

@router.get(
    "/{log_id}",
    response_model=AuditLogDetailResponse,
    dependencies=[
        Depends(require_permission("auditlog.read"))
    ],
)
async def audit_log_detail(
    log_id: UUID,
    db: AsyncSession = DB_SESSION_DEPENDENCY,
    current_user: User = CURRENT_USER_DEPENDENCY,
):
    try :
        return await AuditLogService.detail(db, log_id, current_user)
    except LogNotFoundError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail
        )
    except PermissionDeniedError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail
        )