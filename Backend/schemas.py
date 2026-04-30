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


# -------------------------
# SIMULATION SCHEMAS
# -------------------------

class ROISimulationCreate(BaseModel):
    title: str
    province: str
    annual_kwh: float
    pv_size_kw: float
    installation_cost: float
    electricity_price: float
    incentive_rate: float = 0.0


class SMESimulationCreate(BaseModel):
    title: str
    province: str
    annual_kwh: float
    pv_size_kw: float
    battery_size_kwh: float = 0.0
    installation_cost: float
    electricity_price: float
    incentive_rate: float = 0.0
    company_size: Optional[str] = None
    sector: Optional[str] = None


class SimulationResponse(BaseModel):
    id: int
    user_id: int
    simulation_type: str
    title: str
    input_data: str
    result_data: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# -------------------------
# SUPPLIER / ENERGY SERVICES SCHEMAS
# -------------------------

class SupplierCreate(BaseModel):
    name: str
    category: Literal["audit", "pv", "bess", "cer_support", "consulting"]
    province: str
    description: Optional[str] = None
    verified: bool = False
    plan_tier: str = "free"


class SupplierResponse(BaseModel):
    id: int
    name: str
    category: str
    province: str
    description: Optional[str] = None
    verified: bool
    plan_tier: str

    class Config:
        from_attributes = True


class ContactRequestCreate(BaseModel):
    supplier_id: int
    message: str


class ContactRequestUpdate(BaseModel):
    status: Literal["pending", "responded", "closed"]


class ContactRequestResponse(BaseModel):
    id: int
    user_id: int
    supplier_id: int
    message: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True