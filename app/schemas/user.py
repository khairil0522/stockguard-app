from uuid import UUID
from pydantic import BaseModel, ConfigDict

class UserRead(BaseModel):
    id : UUID
    username : str
    full_name : str
    roles : list[str]
    is_active : bool

class UserDetailRead(BaseModel):
    id: UUID
    username: str
    email: str
    full_name: str
    roles: list[str]
    is_active: bool

class UserCreate(BaseModel):
    username : str
    email : str
    full_name : str
    password : str
    role_id : UUID
    phone_number : str
    address : str
    company_name : str

class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    full_name: str | None = None
    password: str | None = None
    phone_number: str | None = None
    address: str | None = None
    company_name: str | None = None

class UserRoleUpdate(BaseModel):
    role_id: UUID