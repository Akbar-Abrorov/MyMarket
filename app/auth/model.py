from pydantic import BaseModel


class AdminTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AdminRegisterRequest(BaseModel):
    username: str
    password: str


class AdminLoginRequest(BaseModel):
    username: str
    password: str
