from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.health import router as health_router
from .api.auth import router as auth_router
from .config import settings
from .database import engine
from .models.base import Base


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

app.include_router(health_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1/auth")


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
