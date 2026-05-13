import uuid
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Boolean, Column, DateTime, String, Text
from sqlalchemy.types import Enum as SqlEnum
from sqlalchemy.orm import relationship

from .base import Base


class UserRole(str, PyEnum):
    customer = "customer"
    admin = "admin"
    support = "support"


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(120), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=True)
    password_hash = Column(Text, nullable=False)
    role = Column(SqlEnum(UserRole, native_enum=False), nullable=False, default=UserRole.customer)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    tickets = relationship("Ticket", foreign_keys="Ticket.user_id", back_populates="user")
