from uuid import UUID
from pydantic import BaseModel, ConfigDict


class RoleCreate(BaseModel):
    name: str
    description: str | None = None


class RoleUpdate(BaseModel):
    name: str
    description: str | None = None


class RoleRead(BaseModel):
    id: UUID
    name: str
    description: str | None
    is_active: bool
    is_system: bool

    model_config = ConfigDict(from_attributes=True)
