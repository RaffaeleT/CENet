from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr


# -------------------------
# USER SCHEMAS
# -------------------------

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Literal["user", "operator", "supplier", "admin"]


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserRoleSelect(BaseModel):
    role: Literal["user", "operator", "supplier", "admin"]


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
    responded_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class EnergyCommunityCreate(BaseModel):
    name: str
    province: str
    region: Optional[str] = None
    description: Optional[str] = None


class EnergyCommunityResponse(BaseModel):
    id: int
    name: str
    province: str
    region: Optional[str] = None
    description: Optional[str] = None
    status: str
    manager_id: int
    created_at: datetime

    class Config:
        from_attributes = True     
class EventLogCreate(BaseModel):
    event_type: str
    details: Optional[dict] = None


class EventLogResponse(BaseModel):
    id: int
    event_type: str
    user_id: Optional[int] = None
    details: Optional[dict] = None
    created_at: datetime

    class Config:
        from_attributes = True           

# -------------------------
# COMMUNITY / CER MANAGER SCHEMAS
# -------------------------

class EnergyCommunityCreate(BaseModel):
    name: str
    province: str
    region: Optional[str] = None
    description: Optional[str] = None


class EnergyCommunityUpdate(BaseModel):
    name: Optional[str] = None
    province: Optional[str] = None
    region: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Literal["draft", "forming", "active", "paused", "closed"]] = None


class EnergyCommunityResponse(BaseModel):
    id: int
    name: str
    province: str
    region: Optional[str] = None
    description: Optional[str] = None
    status: str
    manager_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class CommunityMemberCreate(BaseModel):
    user_id: int
    member_role: Literal["member", "manager"] = "member"
    pod_id: Optional[str] = None
    status: Literal["invited", "active", "inactive"] = "active"


class CommunityMemberUpdate(BaseModel):
    member_role: Optional[Literal["member", "manager"]] = None
    pod_id: Optional[str] = None
    status: Optional[Literal["invited", "active", "inactive"]] = None


class CommunityMemberResponse(BaseModel):
    id: int
    community_id: int
    user_id: int
    member_role: str
    pod_id: Optional[str] = None
    status: str
    joined_at: datetime

    class Config:
        from_attributes = True


class CommunityDashboardResponse(BaseModel):
    community_id: int
    community_name: str
    status: str
    province: str
    region: Optional[str] = None
    total_members: int
    active_members: int
    invited_members: int
    inactive_members: int
    total_events: int
    recent_events: list[dict]


# -------------------------
# EVENT LOG SCHEMAS
# -------------------------

class EventLogCreate(BaseModel):
    event_type: str
    details: Optional[dict] = None


class EventLogResponse(BaseModel):
    id: int
    event_type: str
    user_id: Optional[int] = None
    details: Optional[dict] = None
    created_at: datetime

    class Config:
        from_attributes = True


# -------------------------
# ADMIN SCHEMAS
# -------------------------

class AdminDashboardResponse(BaseModel):
    total_users: int
    total_communities: int
    total_match_requests: int
    total_simulations: int
    total_suppliers: int
    total_contact_requests: int
    total_events: int
    total_errors: int
    total_api_logs: int

# -------------------------
# SUBSCRIPTION / CONTACT SCHEMAS
# -------------------------

class SubscriptionContactCreate(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    message: Optional[str] = None
    source: Optional[str] = "website"


class SubscriptionContactUpdate(BaseModel):
    status: Literal["new", "contacted", "closed"]


class SubscriptionContactResponse(BaseModel):
    id: int
    email: EmailStr
    name: Optional[str] = None
    message: Optional[str] = None
    source: Optional[str] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True    

# -------------------------
# ERROR LOG SCHEMAS
# -------------------------

class ErrorLogResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    module: Optional[str] = None
    endpoint: str
    error_type: str
    error_message: Optional[str] = None
    timestamp: datetime

    class Config:
        from_attributes = True


# -------------------------
# API PERFORMANCE LOG SCHEMAS
# -------------------------

class APIPerformanceLogResponse(BaseModel):
    id: int
    endpoint: str
    method: str
    status_code: int
    response_time: float
    timestamp: datetime

    class Config:
        from_attributes = True        