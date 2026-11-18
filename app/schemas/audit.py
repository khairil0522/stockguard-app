from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AuditLogRead(BaseModel):
    id: UUID
    actor_type: str
    user_id: UUID | None
    event_type: str
    action: str
    entity_type: str
    entity_id: UUID | None

    model_config = ConfigDict(from_attributes=True)

class AuditLogResponse(BaseModel):
    logs: list[AuditLogRead]
    message: str

class AuditLogDetailResponse(BaseModel):
    id: UUID
    actor_type: str
    user_id: UUID | None
    event_type: str
    action: str
    entity_type: str
    entity_id: UUID | None
    event_metadata: dict | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)