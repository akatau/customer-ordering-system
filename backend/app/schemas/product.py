from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict
from typing import List


class ProductBase(BaseModel):
    name: str
    description: str | None = None
    category: str | None = None
    price: Decimal
    stock_quantity: int


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductListResponse(BaseModel):
    data: List[ProductRead]
    total: int
    page: int
    limit: int
