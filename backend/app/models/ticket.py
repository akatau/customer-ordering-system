from sqlalchemy import Column, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from .base import Base


class TicketStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TicketPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TicketCategory(str, enum.Enum):
    ORDER_ISSUE = "order_issue"
    PRODUCT_QUESTION = "product_question"
    REFUND = "refund"
    SHIPPING = "shipping"
    RETURN = "return"
    OTHER = "other"


class Ticket(Base):
    """Support ticket model for customer inquiries."""
    __tablename__ = "tickets"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    subject = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    
    category = Column(
        Enum(TicketCategory), 
        default=TicketCategory.OTHER, 
        nullable=False
    )
    priority = Column(
        Enum(TicketPriority), 
        default=TicketPriority.MEDIUM, 
        nullable=False
    )
    status = Column(
        Enum(TicketStatus), 
        default=TicketStatus.OPEN, 
        nullable=False,
        index=True
    )
    
    assigned_to = Column(String, ForeignKey("users.id"), nullable=True)
    order_id = Column(String, ForeignKey("orders.id"), nullable=True, index=True)
    
    # Internal notes for support team (JSON array of notes)
    internal_notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="tickets")
    assigned_admin = relationship("User", foreign_keys=[assigned_to])
    order = relationship("Order", back_populates="support_tickets")
