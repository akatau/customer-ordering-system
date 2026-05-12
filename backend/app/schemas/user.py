from pydantic import BaseModel, EmailStr
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

    class Config:
        orm_mode = True
