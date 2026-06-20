from pydantic import BaseModel


class RegisterRequest(BaseModel):
    firstname: str
    lastname: str
    username: str
    password: str
    privilege: int = 0


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"