from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class PermissionCreate(BaseModel):
    code: str
    name: str
    description: str | None = None

class PermissionUpdate(BaseModel):
    name: str
    description: str | None = None

class PermissionRead(BaseModel):
    id: UUID
    code: str
    name: str
    description: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)