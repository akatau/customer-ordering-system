from pydantic import BaseModel, ConfigDict


class CartItemCreate(BaseModel):
    product_id: str
    quantity: int


class CartItemUpdate(BaseModel):
    quantity: int


class CartItemRead(BaseModel):
    product_id: str
    quantity: int
    name: str | None = None
    price: float | None = None

    model_config = ConfigDict(from_attributes=True)


class CartRead(BaseModel):
    user_id: str
    items: list[CartItemRead]
    total: float

    model_config = ConfigDict(from_attributes=True)
