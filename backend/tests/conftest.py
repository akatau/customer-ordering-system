import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Make the backend package importable when pytest runs from the project root
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

# Use an in-memory SQLite database for tests
os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"

from app.main import app  # noqa: E402
from app.database import Base, engine, get_db  # noqa: E402
import app.models.user as _models  # noqa: F401  # Ensure all models are imported before creating tables
import app.models.product as _product_models  # noqa: F401
import app.models.cart as _cart_models  # noqa: F401
import app.models.order as _order_models  # noqa: F401
import app.models.review as _review_models  # noqa: F401
import app.models.admin_log as _admin_log_models  # noqa: F401

@pytest.fixture(scope="function")
def db():
    """Database session fixture."""
    from sqlalchemy.orm import sessionmaker
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
