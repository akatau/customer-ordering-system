from decimal import Decimal
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from ..models.product import Product
from ..core.cache import cache_manager, cache_key, invalidate_products, CACHE_PATTERNS


class ProductService:
    @staticmethod
    def list_products(
        db: Session,
        page: int = 1,
        limit: int = 20,
        q: str | None = None,
        category: str | None = None,
        min_price: Decimal | None = None,
        max_price: Decimal | None = None,
    ) -> tuple[List[Product], int]:
        # Generate cache key from search parameters (Week 7 caching)
        cache_entry_key = cache_key(
            "products:list",
            page=page,
            limit=limit,
            q=q or "",
            category=category or "",
            min_price=float(min_price) if min_price else 0,
            max_price=float(max_price) if max_price else 0,
        )
        
        # Try cache first
        cached = cache_manager.get(cache_entry_key)
        if cached:
            return cached.get("products", []), cached.get("total", 0)
        
        # Cache miss - query database
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

        total = query.count()
        products = query.offset((page - 1) * limit).limit(limit).all()
        
        # Store in cache (1 hour TTL for product catalog)
        cache_manager.set(
            cache_entry_key,
            {"products": products, "total": total},
            cache_type="product_catalog"
        )
        
        return products, total

    @staticmethod
    def get_product(db: Session, product_id: str) -> Product | None:
        # Generate cache key (Week 7 caching)
        cache_entry_key = cache_key("products:detail", product_id)
        
        # Try cache first
        cached = cache_manager.get(cache_entry_key)
        if cached:
            return cached
        
        # Cache miss - query database
        product = db.query(Product).filter(Product.id == product_id).first()
        
        # Store in cache (1 hour TTL for product details)
        if product:
            cache_manager.set(cache_entry_key, product, cache_type="product_catalog")
        
        return product

    @staticmethod
    def create_product(db: Session, payload: Product) -> Product:
        db.add(payload)
        db.commit()
        db.refresh(payload)
        # Invalidate product caches when new product is created (Week 7 cache invalidation)
        invalidate_products()
        return payload
