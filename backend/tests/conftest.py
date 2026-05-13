import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Make the backend package importable when pytest runs from the project root
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

# Use an in-memory SQLite database for tests
os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"

from app.main import app  # noqa: E402
from app.database import Base, get_db  # noqa: E402
import app.models.user as _models  # noqa: F401  # Ensure all models are imported before creating tables
import app.models.product as _product_models  # noqa: F401
import app.models.cart as _cart_models  # noqa: F401
import app.models.order as _order_models  # noqa: F401
import app.models.review as _review_models  # noqa: F401
import app.models.admin_log as _admin_log_models  # noqa: F401

from sqlalchemy import create_engine

TEST_DATABASE_URL = "sqlite+pysqlite:///:memory:"


@pytest.fixture(scope="function")
def db():
    """Create a fresh in-memory SQLite database for each test."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    Base.metadata.create_all(bind=engine)
    connection = engine.connect()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()
        connection.close()
        engine.dispose()


@pytest.fixture(scope="function")
def client(db):
    """Test client that uses the transactional test database."""
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
