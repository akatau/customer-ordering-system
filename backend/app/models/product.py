import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, DateTime, Numeric, String, Text
from sqlalchemy.orm import relationship
from .base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(String(120), nullable=True, index=True)
    image_url = Column(String(1024), nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    stock_quantity = Column(Numeric(10, 0), nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    cart_items = relationship("CartItem", back_populates="product")
