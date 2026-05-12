from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from .config import settings
from .models.base import Base

connect_args = {}
poolclass = None

if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
    poolclass = StaticPool

engine = create_engine(
    settings.database_url,
    future=True,
    echo=False,
    pool_pre_ping=True,
    connect_args=connect_args,
    poolclass=poolclass,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
