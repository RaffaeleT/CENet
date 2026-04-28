from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)

    # local login users have a password, social users can have None
    password = Column(String, nullable=True)

    # role is NULL until first-time onboarding is completed
    role = Column(String, nullable=True, default=None)

    # social auth fields
    auth_provider = Column(String, nullable=True)   # google / microsoft / linkedin / local
    provider_sub = Column(String, nullable=True)    # provider-specific user id
    full_name = Column(String, nullable=True)

    match_requests = relationship("MatchRequest", back_populates="user")
    simulations = relationship("Simulation", back_populates="user")


class MatchRequest(Base):
    __tablename__ = "match_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    province = Column(String, nullable=False)
    need_type = Column(String, nullable=False)
    message = Column(Text, nullable=True)
    status = Column(String, nullable=False, default="pending")

    user = relationship("User", back_populates="match_requests")


class Simulation(Base):
    __tablename__ = "simulations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    input_data = Column(Text, nullable=False)
    result_data = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="simulations")