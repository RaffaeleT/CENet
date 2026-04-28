from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr


# -------------------------
# USER SCHEMAS
# -------------------------

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Literal["user", "operator", "supplier"]


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserRoleSelect(BaseModel):
    role: Literal["user", "operator", "supplier"]


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: Optional[str] = None
    full_name: Optional[str] = None
    auth_provider: Optional[str] = None

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class MessageResponse(BaseModel):
    message: str


# -------------------------
# SIMULATION SCHEMAS
# -------------------------

class SimulationCreate(BaseModel):
    title: str
    input_data: str


class SimulationResponse(BaseModel):
    id: int
    title: str
    input_data: str
    result_data: Optional[str] = None
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True


# -------------------------
# MATCHING SCHEMAS
# -------------------------

class MatchRequestCreate(BaseModel):
    province: str
    need_type: str
    message: Optional[str] = None


class MatchRequestResponse(BaseModel):
    id: int
    user_id: int
    province: str
    need_type: str
    message: Optional[str] = None
    status: str

    class Config:
        from_attributes = True