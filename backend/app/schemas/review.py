from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class ReviewCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: str | None = Field(None, max_length=500)


class ReviewRead(BaseModel):
    id: str
    user_id: str
    product_id: str
    rating: int
    comment: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
