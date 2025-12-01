from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")


class TokenPayload(BaseModel):
    sub: Optional[str] = Field(None, description="Subject (user id/email)")
    exp: Optional[int] = Field(None, description="Expiration timestamp")


class UserBase(BaseModel):
    email: EmailStr = Field(..., description="User email")
    full_name: Optional[str] = Field(None, description="Full name")


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="Password")


class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="User email for login")
    password: str = Field(..., min_length=6, description="Password for login")


class UserPublic(UserBase):
    id: int = Field(..., description="User identifier")
    is_active: bool = Field(..., description="Is user active")
