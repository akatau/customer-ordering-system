from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..api.deps import get_db
from ..schemas.product import ProductCreate, ProductListResponse, ProductRead
from ..models.product import Product
from ..services.product_service import ProductService
from typing import List

router = APIRouter(tags=["Products"])


@router.get("/", response_model=ProductListResponse)
def list_products(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    q: str | None = Query(None, description="Search query for product name or description"),
    category: str | None = Query(None, description="Filter by category"),
    sort: str | None = Query(None, description="Sort by price_asc or price_desc"),
    min_price: Decimal | None = Query(None, description="Minimum product price"),
    max_price: Decimal | None = Query(None, description="Maximum product price"),
) -> ProductListResponse:
    products, total = ProductService.list_products(
        db,
        page=page,
        limit=limit,
        q=q,
        category=category,
        sort=sort,
        min_price=min_price,
        max_price=max_price,
    )
    return ProductListResponse(data=products, total=total, page=page, limit=limit)


@router.get("/search", response_model=list[ProductRead])
def search_products(
    db: Session = Depends(get_db),
    q: str = Query(..., min_length=1, description="Search query for product name or description"),
    limit: int = Query(10, ge=1, le=100),
    sort: str | None = Query(None, description="Sort by price_asc or price_desc"),
) -> list[ProductRead]:
    products, _ = ProductService.list_products(db, page=1, limit=limit, q=q, sort=sort)
    return products




@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)) -> ProductRead:
    product = Product(
        name=payload.name,
        description=payload.description,
        category=payload.category,
        price=payload.price,
        stock_quantity=payload.stock_quantity,
    )
    return ProductService.create_product(db, product)


@router.get('/categories', response_model=List[str])
def get_categories(db: Session = Depends(get_db)) -> List[str]:
    return ProductService.get_categories(db)


@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: str, db: Session = Depends(get_db)) -> ProductRead:
    product = ProductService.get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product
