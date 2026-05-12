from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict
from typing import List


class OrderItemCreate(BaseModel):
    product_id: str
    quantity: int


class OrderCreate(BaseModel):
    shipping_address: str
    billing_address: str | None = None
    payment_method: str
    items: List[OrderItemCreate]


class OrderItemRead(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    unit_price: Decimal
    total_price: Decimal

    model_config = ConfigDict(from_attributes=True)


class OrderRead(BaseModel):
    id: str
    user_id: str
    shipping_address: str
    billing_address: str | None = None
    status: str
    total_amount: Decimal
    items: List[OrderItemRead]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
