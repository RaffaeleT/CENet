from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)

    # Local login users have a password, social users can have None
    password = Column(String, nullable=True)

    # Role is NULL until first-time onboarding is completed
    role = Column(String, nullable=True, default=None)

    # Social auth fields
    auth_provider = Column(String, nullable=True, default="local")
    provider_sub = Column(String, nullable=True)
    full_name = Column(String, nullable=True)

    match_requests = relationship(
        "MatchRequest",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    simulations = relationship(
        "Simulation",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    contact_requests = relationship(
        "ContactRequest",
        back_populates="user",
        cascade="all, delete-orphan"
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

    user = relationship("User", back_populates="match_requests")

    def __repr__(self):
        return f"<MatchRequest id={self.id} user_id={self.user_id} status={self.status}>"


class Simulation(Base):
    __tablename__ = "simulations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    simulation_type = Column(String, nullable=False)  # roi / sme
    title = Column(String, nullable=False)
    input_data = Column(Text, nullable=False)
    result_data = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="simulations")

    def __repr__(self):
        return f"<Simulation id={self.id} user_id={self.user_id} type={self.simulation_type}>"


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
        cascade="all, delete-orphan"
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

    user = relationship("User", back_populates="contact_requests")
    supplier = relationship("Supplier", back_populates="contact_requests")

    def __repr__(self):
        return f"<ContactRequest id={self.id} user_id={self.user_id} supplier_id={self.supplier_id}>"
    

class EnergyCommunity(Base):
    __tablename__ = "energy_communities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    province = Column(String, nullable=False)
    region = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    status = Column(String, nullable=False, default="draft")
    manager_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)    
    
from sqlalchemy import JSON

class EventLog(Base):
    __tablename__ = "event_logs"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)    