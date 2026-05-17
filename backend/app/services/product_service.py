from decimal import Decimal
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import or_, func, asc, desc

from ..models.product import Product


class ProductService:
    @staticmethod
    def list_products(
        db: Session,
        page: int = 1,
        limit: int = 20,
        q: str | None = None,
        category: str | None = None,
        sort: str | None = None,
        min_price: Decimal | None = None,
        max_price: Decimal | None = None,
    ) -> tuple[List[Product], int]:
        query = db.query(Product)

        if q:
            search_term = f"%{q}%"
            query = query.filter(or_(Product.name.ilike(search_term), Product.description.ilike(search_term)))

        if category:
            query = query.filter(Product.category == category)

        if min_price is not None:
            query = query.filter(Product.price >= min_price)

        if max_price is not None:
            query = query.filter(Product.price <= max_price)

        if sort == "price_asc":
            query = query.order_by(asc(Product.price))
        elif sort == "price_desc":
            query = query.order_by(desc(Product.price))
        else:
            query = query.order_by(Product.created_at.desc())

        total = query.count()
        products = query.offset((page - 1) * limit).limit(limit).all()
        return products, total

    @staticmethod
    def get_product(db: Session, product_id: str) -> Product | None:
        return db.query(Product).filter(Product.id == product_id).first()

    @staticmethod
    def create_product(db: Session, payload: Product) -> Product:
        db.add(payload)
        db.commit()
        db.refresh(payload)
        return payload

    @staticmethod
    def get_categories(db: Session) -> List[str]:
        # Return distinct, non-null categories
        results = db.query(func.distinct(Product.category)).filter(Product.category.isnot(None)).all()
        # results is list of tuples like [(category,), ...]
        return [r[0] for r in results if r[0]]
