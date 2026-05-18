from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.health import router as health_router
from .api.auth import router as auth_router
from .api.products import router as products_router
from .api.cart import router as cart_router
from .api.orders import router as orders_router
from .api.reviews import router as reviews_router
from .api.users import router as users_router
from .api.admin import router as admin_router
from .config import settings
from .database import engine
from .models import user, product, cart, order, review, admin_log  # noqa: F401
from .models.base import Base


app = FastAPI(
    title=settings.app_name,
    description="Backend API for the Customer Ordering Sub-system",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    # Allow all origins during local development to avoid CORS issues
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1/auth")
app.include_router(products_router, prefix="/api/v1/products")
app.include_router(cart_router, prefix="/api/v1/cart")
app.include_router(orders_router, prefix="/api/v1/orders")
app.include_router(reviews_router, prefix="/api/v1/reviews")
app.include_router(users_router, prefix="/api/v1/users")
app.include_router(admin_router, prefix="/api/v1")


@app.on_event("startup")
def startup_event():
    # Avoid forcing a PostgreSQL connection during test startup.
    # Test fixtures create the in-memory schema themselves.
    if settings.database_url.startswith("sqlite"):
        Base.metadata.create_all(bind=engine)
