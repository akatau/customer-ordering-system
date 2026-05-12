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
from app.database import Base, engine  # noqa: E402
import app.models.user as _models  # noqa: F401  # Ensure all models are imported before creating tables

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(app)
