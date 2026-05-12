from pydantic import BaseModel, ConfigDict, EmailStr
from uuid import UUID
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str | None = None
    role: str
    is_active: bool


class UserCreate(UserBase):
    password: str


class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    username: str
    full_name: str | None = None
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
