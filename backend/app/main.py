from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware

from .api.health import router as health_router
from .api.auth import router as auth_router
from .api.products import router as products_router
from .api.cart import router as cart_router
from .api.orders import router as orders_router
from .api.reviews import router as reviews_router
from .api.users import router as users_router
from .api.admin import router as admin_router
from .api.support import router as support_router
from .api.reporting import router as reporting_router
from .config import settings
from .database import engine
from .models import user, product, cart, order, review, admin_log, ticket  # noqa: F401
from .models.base import Base
from .core.cache import cache_manager


app = FastAPI(
    title=settings.app_name,
    description="Backend API for the Customer Ordering Sub-system",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add GZIP compression for responses > 1KB (Week 7 optimization)
app.add_middleware(GZipMiddleware, minimum_size=1000)

app.include_router(health_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1/auth")
app.include_router(products_router, prefix="/api/v1/products")
app.include_router(cart_router, prefix="/api/v1/cart")
app.include_router(orders_router, prefix="/api/v1/orders")
app.include_router(reviews_router, prefix="/api/v1/reviews")
app.include_router(users_router, prefix="/api/v1/users")
app.include_router(support_router, prefix="/api/v1/support")
app.include_router(reporting_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1")


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    # Verify cache connection (Week 7 optimization)
    if cache_manager.is_available():
        cache_stats = cache_manager.get_stats()
        print(f"Cache connected: {cache_stats}")
