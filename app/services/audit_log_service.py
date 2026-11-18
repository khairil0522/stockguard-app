from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.errors.auth import LogNotFoundError, PermissionDeniedError
from app.models.audit_logs import AuditLog
from app.models.users import User
from app.repositories.user_repository import user_repository
from app.schemas.audit import AuditLogDetailResponse, AuditLogRead, AuditLogResponse


class AuditLogService:
    @staticmethod
    async def log(
        db: AsyncSession,
        *,
        actor_type: str,
        user_id: UUID | None = None,
        event_type: str,
        action: str,
        entity_type: str | None = None,
        entity_id: UUID | None = None,
        description: str,
        event_metadata: dict | None = None,
        severity: str = "INFO",
    ) -> AuditLog:

        audit_log = AuditLog(
            actor_type=actor_type,
            user_id=user_id,
            event_type=event_type,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            description=description,
            event_metadata=event_metadata,
            severity=severity,
        )

        db.add(audit_log)
        await db.flush()

        return audit_log

    async def show(db : AsyncSession):
        result = await db.execute(
            select(AuditLog)
        )

        logs = result.scalars().all()

        if not logs:
            return AuditLogResponse(
                logs=[],
                message="No log"
            )

        return AuditLogResponse(
            logs=[
                AuditLogRead.model_validate(log)
                for log in logs
            ],
            message="Log Appeared"
        )

    async def detail(db: AsyncSession, log_id: UUID, current_user: User):
        current_roles = set(
                await user_repository.get_role_names(db, current_user.id)
        )

        if "SUPERADMIN" not in current_roles:
            raise PermissionDeniedError()

        result = await db.execute(
            select(AuditLog).where(AuditLog.id == log_id)
        )

        log = result.scalar_one_or_none()

        if not log:
            raise LogNotFoundError()

        return AuditLogDetailResponse.model_validate(log)