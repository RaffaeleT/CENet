from datetime import datetime
from typing import Any, Literal, Optional

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
    responded_at: Optional[datetime] = None

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
    recent_events: list[dict[str, Any]]


# -------------------------
# EVENT LOG SCHEMAS
# -------------------------

class EventLogCreate(BaseModel):
    event_type: str
    details: Optional[dict[str, Any]] = None


class EventLogResponse(BaseModel):
    id: int
    event_type: str
    user_id: Optional[int] = None
    details: Optional[dict[str, Any]] = None
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
    endpoint: Optional[str] = None
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


# -------------------------
# REC ENERGY SCHEMAS
# -------------------------

class RECEnergyUploadResponse(BaseModel):
    id: int
    community_id: int
    uploaded_by: int
    filename: str
    file_type: str
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None
    status: str
    validation_errors: Optional[dict] = None
    created_at: datetime

    class Config:
        from_attributes = True


class RECKPIResponse(BaseModel):
    community_id: int
    total_produced_kwh: float
    total_consumed_kwh: float
    total_shared_kwh: float
    self_consumption_percentage: float


class RECTrendResponse(BaseModel):
    period: str
    produced_kwh: float
    consumed_kwh: float
    shared_kwh: float


class RECMemberEnergyResponse(BaseModel):
    pod_id: str
    produced_kwh: float
    consumed_kwh: float
    shared_kwh: float


# -------------------------
# PERSONAL ENERGY SCHEMAS
# -------------------------

class PersonalEnergyUploadResponse(BaseModel):
    id: int
    user_id: int
    filename: str
    file_type: str
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None
    status: str
    validation_errors: Optional[dict] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ManualEnergyInputCreate(BaseModel):
    annual_consumption_kwh: float
    system_power_kw: Optional[float] = None
    province: Optional[str] = None


class ManualEnergyInputResponse(BaseModel):
    id: int
    user_id: int
    annual_consumption_kwh: float
    system_power_kw: Optional[float] = None
    province: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class PersonalKPIResponse(BaseModel):
    user_id: int
    total_consumed_kwh: float
    total_produced_kwh: float
    total_fed_to_grid_kwh: float
    total_self_consumed_kwh: float
    average_monthly_consumption_kwh: float
    self_consumption_percentage: float


# -------------------------
# REC INCENTIVE SCHEMAS
# -------------------------

class EnergyPriceCreate(BaseModel):
    price_eur_kwh: float
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None


class EnergyPriceResponse(BaseModel):
    id: int
    community_id: int
    price_eur_kwh: float
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True


class CommunityCostCreate(BaseModel):
    fixed_management_cost: float = 0.0
    variable_cost: float = 0.0


class CommunityCostResponse(BaseModel):
    id: int
    community_id: int
    fixed_management_cost: float
    variable_cost: float
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True


class GSEIncentiveParameterCreate(BaseModel):
    name: str
    tariff_eur_kwh: float
    description: Optional[str] = None
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None


class GSEIncentiveParameterResponse(BaseModel):
    id: int
    name: str
    tariff_eur_kwh: float
    description: Optional[str] = None
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class IncentiveAllocationResponse(BaseModel):
    id: int
    community_id: int
    member_user_id: int
    gross_incentive: float
    cost_share: float
    net_reimbursement: float
    created_at: datetime

    class Config:
        from_attributes = True


# -------------------------
# NEWSLETTER SCHEMAS
# -------------------------

class NewsletterSubscribeCreate(BaseModel):
    email: str
    name: Optional[str] = None
    user_type: Optional[str] = None
    preferences: Optional[dict] = None


class NewsletterSubscriberResponse(BaseModel):
    id: int
    email: str
    name: Optional[str] = None
    user_type: Optional[str] = None
    preferences: Optional[dict] = None
    is_active: bool
    unsubscribed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True