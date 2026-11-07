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