from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)

    # Local login users have a password. Social login users can have None.
    password = Column(String, nullable=True)

    # Role is NULL until first-time onboarding is completed.
    role = Column(String, nullable=True, default=None)

    # Social auth fields
    auth_provider = Column(String, nullable=True, default="local")
    provider_sub = Column(String, nullable=True)
    full_name = Column(String, nullable=True)

    # Extra profile/reporting fields
    province = Column(String, nullable=True)
    user_type = Column(String, nullable=True)  # individual / condominium / sme / cer_operator
    ateco_sector = Column(String, nullable=True)
    email_confirmed = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    last_login_at = Column(DateTime, nullable=True)

    match_requests = relationship(
        "MatchRequest",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    simulations = relationship(
        "Simulation",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    contact_requests = relationship(
        "ContactRequest",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<User id={self.id} email={self.email} role={self.role}>"


class MatchRequest(Base):
    __tablename__ = "match_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    province = Column(String, nullable=False)
    need_type = Column(String, nullable=False)
    message = Column(Text, nullable=True)
    status = Column(String, nullable=False, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="match_requests")

    def __repr__(self):
        return f"<MatchRequest id={self.id} province={self.province} status={self.status}>"


class Simulation(Base):
    __tablename__ = "simulations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    simulation_type = Column(String, nullable=False)  # roi / sme / public_roi
    title = Column(String, nullable=False)
    input_data = Column(Text, nullable=False)
    result_data = Column(Text, nullable=True)

    status = Column(String, nullable=False, default="completed")  # started / completed / failed
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    execution_time = Column(Float, nullable=True)  # milliseconds

    user = relationship("User", back_populates="simulations")

    def __repr__(self):
        return f"<Simulation id={self.id} type={self.simulation_type} title={self.title}>"


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)  # audit / pv / bess / cer_support / consulting
    province = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    verified = Column(Boolean, default=False)
    plan_tier = Column(String, nullable=False, default="free")

    contact_requests = relationship(
        "ContactRequest",
        back_populates="supplier",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Supplier id={self.id} name={self.name} category={self.category}>"


class ContactRequest(Base):
    __tablename__ = "contact_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id", ondelete="CASCADE"), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(String, nullable=False, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    responded_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="contact_requests")
    supplier = relationship("Supplier", back_populates="contact_requests")

    def __repr__(self):
        return f"<ContactRequest id={self.id} status={self.status}>"


class EnergyCommunity(Base):
    __tablename__ = "energy_communities"

    id = Column(Integer, primary_key=True, index=True)
    community_code = Column(String, unique=True, nullable=True, index=True)

    name = Column(String, nullable=False)
    province = Column(String, nullable=False)
    region = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    status = Column(String, nullable=False, default="draft")
    manager_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<EnergyCommunity id={self.id} name={self.name} status={self.status}>"


class CommunityMember(Base):
    __tablename__ = "community_members"

    id = Column(Integer, primary_key=True, index=True)
    community_id = Column(Integer, ForeignKey("energy_communities.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    member_role = Column(String, nullable=False, default="member")  # member / manager
    pod_id = Column(String, nullable=True)
    status = Column(String, nullable=False, default="active")  # invited / active / inactive
    joined_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<CommunityMember id={self.id} community_id={self.community_id} user_id={self.user_id}>"


class EventLog(Base):
    __tablename__ = "event_logs"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<EventLog id={self.id} type={self.event_type}>"


class ModuleUsage(Base):
    __tablename__ = "module_usage"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    module_name = Column(String, nullable=False, index=True)  # roi / sme / matching / energy_services / cer_manager
    action = Column(String, nullable=False)  # started / completed / failed / abandoned
    details = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ModuleUsage id={self.id} module={self.module_name} action={self.action}>"


class ErrorLog(Base):
    __tablename__ = "error_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    module = Column(String, nullable=True)
    endpoint = Column(String, nullable=True)
    error_type = Column(String, nullable=False)
    error_message = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ErrorLog id={self.id} type={self.error_type}>"


class APIPerformanceLog(Base):
    __tablename__ = "api_performance_logs"

    id = Column(Integer, primary_key=True, index=True)
    endpoint = Column(String, nullable=False)
    method = Column(String, nullable=False)
    status_code = Column(Integer, nullable=False)
    response_time = Column(Float, nullable=False)  # milliseconds
    timestamp = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<APIPerformanceLog id={self.id} endpoint={self.endpoint} status={self.status_code}>"


class SubscriptionContact(Base):
    __tablename__ = "subscription_contacts"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, index=True)
    name = Column(String, nullable=True)
    message = Column(Text, nullable=True)
    source = Column(String, nullable=True, default="website")
    status = Column(String, nullable=False, default="new")
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<SubscriptionContact id={self.id} email={self.email} status={self.status}>"


# -------------------------
# REC ENERGY DATA
# -------------------------

class RECEnergyUpload(Base):
    __tablename__ = "rec_energy_uploads"

    id = Column(Integer, primary_key=True, index=True)
    community_id = Column(Integer, ForeignKey("energy_communities.id", ondelete="CASCADE"), nullable=False)
    uploaded_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)  # csv / xlsx

    period_start = Column(DateTime, nullable=True)
    period_end = Column(DateTime, nullable=True)

    status = Column(String, nullable=False, default="uploaded")  # uploaded / validated / failed / replaced
    validation_errors = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<RECEnergyUpload id={self.id} community_id={self.community_id} status={self.status}>"


class RECEnergyReading(Base):
    __tablename__ = "rec_energy_readings"

    id = Column(Integer, primary_key=True, index=True)
    community_id = Column(Integer, ForeignKey("energy_communities.id", ondelete="CASCADE"), nullable=False)
    upload_id = Column(Integer, ForeignKey("rec_energy_uploads.id", ondelete="CASCADE"), nullable=False)

    pod_id = Column(String, nullable=True)
    reading_date = Column(DateTime, nullable=False)

    kwh_produced = Column(Float, nullable=False, default=0)
    kwh_consumed = Column(Float, nullable=False, default=0)
    kwh_shared = Column(Float, nullable=False, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<RECEnergyReading id={self.id} pod_id={self.pod_id} date={self.reading_date}>"


# -------------------------
# PERSONAL ENERGY DATA
# -------------------------

class PersonalEnergyUpload(Base):
    __tablename__ = "personal_energy_uploads"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)

    period_start = Column(DateTime, nullable=True)
    period_end = Column(DateTime, nullable=True)

    status = Column(String, nullable=False, default="uploaded")
    validation_errors = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<PersonalEnergyUpload id={self.id} user_id={self.user_id} status={self.status}>"


class PersonalEnergyReading(Base):
    __tablename__ = "personal_energy_readings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    upload_id = Column(Integer, ForeignKey("personal_energy_uploads.id", ondelete="CASCADE"), nullable=True)

    pod_id = Column(String, nullable=True)
    reading_date = Column(DateTime, nullable=False)

    kwh_consumed = Column(Float, nullable=False, default=0)
    kwh_produced = Column(Float, nullable=False, default=0)
    kwh_fed_to_grid = Column(Float, nullable=False, default=0)
    kwh_self_consumed = Column(Float, nullable=False, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<PersonalEnergyReading id={self.id} user_id={self.user_id} date={self.reading_date}>"


class ManualEnergyInput(Base):
    __tablename__ = "manual_energy_inputs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    annual_consumption_kwh = Column(Float, nullable=False)
    system_power_kw = Column(Float, nullable=True)
    province = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ManualEnergyInput id={self.id} user_id={self.user_id} annual_consumption={self.annual_consumption_kwh}>"


# -------------------------
# ENERGY PRICES / INCENTIVES
# -------------------------

class EnergyPrice(Base):
    __tablename__ = "energy_prices"

    id = Column(Integer, primary_key=True, index=True)
    community_id = Column(Integer, ForeignKey("energy_communities.id", ondelete="CASCADE"), nullable=True)

    price_eur_kwh = Column(Float, nullable=False)
    valid_from = Column(DateTime, nullable=False)
    valid_to = Column(DateTime, nullable=True)

    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<EnergyPrice id={self.id} price={self.price_eur_kwh}>"


class GSEIncentiveParameter(Base):
    __tablename__ = "gse_incentive_parameters"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    tariff_eur_kwh = Column(Float, nullable=False)
    description = Column(Text, nullable=True)

    valid_from = Column(DateTime, nullable=True)
    valid_to = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<GSEIncentiveParameter id={self.id} name={self.name} tariff={self.tariff_eur_kwh}>"


class CommunityCost(Base):
    __tablename__ = "community_costs"

    id = Column(Integer, primary_key=True, index=True)
    community_id = Column(Integer, ForeignKey("energy_communities.id", ondelete="CASCADE"), nullable=False)

    fixed_management_cost = Column(Float, nullable=False, default=0)
    variable_cost = Column(Float, nullable=False, default=0)

    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<CommunityCost id={self.id} community_id={self.community_id}>"


class IncentiveAllocation(Base):
    __tablename__ = "incentive_allocations"

    id = Column(Integer, primary_key=True, index=True)
    community_id = Column(Integer, ForeignKey("energy_communities.id", ondelete="CASCADE"), nullable=False)
    member_user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    period_start = Column(DateTime, nullable=True)
    period_end = Column(DateTime, nullable=True)

    gross_incentive = Column(Float, nullable=False, default=0)
    cost_share = Column(Float, nullable=False, default=0)
    net_reimbursement = Column(Float, nullable=False, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<IncentiveAllocation id={self.id} community_id={self.community_id} member_user_id={self.member_user_id}>"


# -------------------------
# ROI PARAMETERS
# -------------------------

class CalculationParameter(Base):
    __tablename__ = "calculation_parameters"

    id = Column(Integer, primary_key=True, index=True)
    parameter_name = Column(String, unique=True, nullable=False)
    parameter_value = Column(Float, nullable=False)
    unit = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<CalculationParameter id={self.id} name={self.parameter_name} value={self.parameter_value}>"


# -------------------------
# NEWSLETTER
# -------------------------

class NewsletterSubscriber(Base):
    __tablename__ = "newsletter_subscribers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False, index=True)
    user_type = Column(String, nullable=True)
    preferences = Column(JSON, nullable=True)

    is_active = Column(Boolean, default=True)
    unsubscribe_token = Column(String, unique=True, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    unsubscribed_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<NewsletterSubscriber id={self.id} email={self.email} active={self.is_active}>"