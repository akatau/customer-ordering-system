from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class AdminLogResponse(BaseModel):
    id: str
    admin_user_id: str
    action: str
    resource_type: str
    resource_id: Optional[str]
    details: Optional[dict]
    ip_address: Optional[str]
    timestamp: datetime

    class Config:
        from_attributes = True


class AdminLogListResponse(BaseModel):
    logs: List[AdminLogResponse]


class ProductCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    category: str = Field(..., min_length=1, max_length=100)
    stock_quantity: int = Field(..., ge=0)
    image_url: Optional[str] = None


class ProductUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    stock_quantity: Optional[int] = Field(None, ge=0)
    image_url: Optional[str] = None


class UserAdminResponse(BaseModel):
    id: str
    email: str
    username: str
    full_name: Optional[str]
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserAdminListResponse(BaseModel):
    users: List[UserAdminResponse]


class UserUpdateAdminRequest(BaseModel):
    full_name: Optional[str] = None
    role: Optional[str] = Field(None, pattern="^(customer|admin|support)$")
    is_active: Optional[bool] = None


class OrderAdminResponse(BaseModel):
    id: str
    user_id: str
    status: str
    total_amount: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OrderAdminListResponse(BaseModel):
    orders: List[OrderAdminResponse]


class OrderUpdateAdminRequest(BaseModel):
    status: str = Field(..., pattern="^(pending|processing|completed|cancelled)$")


class BulkImportResponse(BaseModel):
    imported_count: int
    errors: List[str]


class ExportResponse(BaseModel):
    export_url: str
    message: str
