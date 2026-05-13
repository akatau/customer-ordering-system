from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserProfileUpdate(BaseModel):
    full_name: str | None = Field(None, max_length=255)
    username: str | None = Field(None, min_length=3, max_length=120)


class UserProfileRead(BaseModel):
    id: str
    email: EmailStr
    username: str
    full_name: str | None = None
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)
