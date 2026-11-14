import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, String, func, CheckConstraint, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class ActorType(str, Enum):
    USER = "USER"
    SYSTEM = "SYSTEM"

class EventType(str, Enum):
    ACTIVITY = "ACTIVITY"
    SECURITY = "SECURITY"
    FRAUD = "FRAUD"

class Severity(str, Enum):
    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    actor_type: Mapped[ActorType] = mapped_column(
        String(20),
        nullable=False,
    )

    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )

    event_type: Mapped[EventType] = mapped_column(
        String(20),
        nullable=False,
    )

    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    entity_type: Mapped[str] = mapped_column(
        String(50),
        nullable=True,
    )

    entity_id: Mapped[uuid.UUID | None] = mapped_column(
    UUID(as_uuid=True),
    nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
    String(255),
    nullable=False,
    )

    event_metadata: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    severity: Mapped[Severity] = mapped_column(
        String(20),
        nullable=False,
        default=Severity.INFO,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

