import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text, JSON

from .base import Base


class AdminLog(Base):
    __tablename__ = "admin_logs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    admin_user_id = Column(String(36), nullable=False, index=True)
    action = Column(String(100), nullable=False, index=True)
    resource_type = Column(String(50), nullable=False)  # e.g., 'product', 'user', 'order'
    resource_id = Column(String(36), nullable=True)
    details = Column(JSON, nullable=True)  # Additional context as JSON
    ip_address = Column(String(45), nullable=True)  # IPv4/IPv6
    user_agent = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<AdminLog(id={self.id}, action={self.action}, resource_type={self.resource_type})>"