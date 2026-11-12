from uuid import UUID
from pydantic import BaseModel, ConfigDict

class RolePermissionAssign(BaseModel):
    permission_ids: list[UUID]


class RolePermissionRemove(BaseModel):
    permission_ids: list[UUID]


class RolePermissionRead(BaseModel):
    permission_id: UUID
    permission_code: str
    assigned: bool