from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field


class LocalLoginRequest(BaseModel):
    login_id: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class TokenResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"
    expires_in: int


class GoogleLoginUrlResponse(BaseModel):
    authorization_url: str


class RefreshRequest(BaseModel):
    # Cookie ベース運用のためボディは不要だが、空のモデルで 422 を避ける
    pass


class LogoutResponse(BaseModel):
    detail: str


class AuthSuccessResponse(BaseModel):
    token: TokenResponse
    user_id: int
    role: str
    full_name: str
    email: EmailStr
    session_token: str
    issued_at: datetime
