from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone
from nanoid import generate
from uuid import UUID

from app.models import AuditLog

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