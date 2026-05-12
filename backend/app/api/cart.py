from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..api.deps import get_current_user, get_db
from ..schemas.cart import CartItemCreate, CartItemRead, CartItemUpdate, CartRead
from ..services.cart_service import CartService

router = APIRouter(tags=["Cart"])


@router.get("/", response_model=CartRead)
def get_cart(user=Depends(get_current_user), db: Session = Depends(get_db)) -> CartRead:
    cart = CartService.get_cart(db, user)
    items = []
    total = 0.0
    for item in cart.items:
        items.append(
            CartItemRead(
                product_id=item.product_id,
                quantity=item.quantity,
                name=item.product.name if item.product else None,
                price=float(item.product.price) if item.product else None,
            )
        )
        total += float(item.product.price) * item.quantity if item.product else 0.0
    return CartRead(user_id=user.id, items=items, total=total)


@router.post("/items", response_model=CartRead, status_code=status.HTTP_201_CREATED)
def add_cart_item(payload: CartItemCreate, user=Depends(get_current_user), db: Session = Depends(get_db)) -> CartRead:
    try:
        cart = CartService.add_item(db, user, payload.product_id, payload.quantity)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return get_cart(user, db)


@router.put("/items/{product_id}", response_model=CartRead)
def update_cart_item(product_id: str, payload: CartItemUpdate, user=Depends(get_current_user), db: Session = Depends(get_db)) -> CartRead:
    try:
        CartService.update_item(db, user, product_id, payload.quantity)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return get_cart(user, db)


@router.delete("/items/{product_id}", response_model=CartRead)
def remove_cart_item(product_id: str, user=Depends(get_current_user), db: Session = Depends(get_db)) -> CartRead:
    try:
        CartService.remove_item(db, user, product_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return get_cart(user, db)


@router.post("/clear", response_model=CartRead)
def clear_cart(user=Depends(get_current_user), db: Session = Depends(get_db)) -> CartRead:
    CartService.clear_cart(db, user)
    return get_cart(user, db)
