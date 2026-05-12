from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..api.deps import get_current_user, get_db
from ..schemas.order import OrderCreate, OrderRead
from ..services.order_service import OrderService

router = APIRouter(tags=["Orders"])


@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderCreate, user=Depends(get_current_user), db: Session = Depends(get_db)) -> OrderRead:
    try:
        order = OrderService.create_order(
            db,
            user_id=user.id,
            shipping_address=payload.shipping_address,
            billing_address=payload.billing_address,
            payment_method=payload.payment_method,
            items_data=[item.model_dump() for item in payload.items],
        )
        return order
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/", response_model=list[OrderRead])
def list_orders(user=Depends(get_current_user), db: Session = Depends(get_db)) -> list[OrderRead]:
    return OrderService.list_orders(db, user.id)


@router.get("/{order_id}", response_model=OrderRead)
def get_order(order_id: str, user=Depends(get_current_user), db: Session = Depends(get_db)) -> OrderRead:
    order = OrderService.get_order(db, user.id, order_id)
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order
