from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

class UserMeResponse(BaseModel):
    id: str
    username: str
    email: str
    full_name: str
    is_active: bool

class RegisterRequest(BaseModel):
    username: str
    email: str
    full_name: str
    password: str
    phone_number: str | None = None
    address: str | None = None
    company_name: str | None = None

class RegisterResponse(BaseModel):
    access_token: str
    token_type: str
    username: str