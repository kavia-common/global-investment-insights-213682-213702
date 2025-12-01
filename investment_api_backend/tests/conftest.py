import os
import sys
from typing import Generator

# -----------------------------------------------------------------------------
# Ensure backend root is on sys.path BEFORE any other imports.
# Compute BASE_DIR as the parent of tests/ (i.e., investment_api_backend/)
# so that 'src' can be imported as a package without relying on external PYTHONPATH.
# -----------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402

from src.api.main import app  # noqa: E402
from src.db.session import Base, get_db  # noqa: E402
from src.db import models  # noqa: E402

# Use a SQLite DB for tests to avoid external dependency
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite:///./test_db.sqlite3")

# Create test engine and session
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False} if TEST_DATABASE_URL.startswith("sqlite") else {},
    pool_pre_ping=True,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db() -> Generator:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def db_setup_and_teardown():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop all tables after tests
    Base.metadata.drop_all(bind=engine)
    # Remove SQLite file if used
    if TEST_DATABASE_URL.startswith("sqlite") and TEST_DATABASE_URL.endswith("test_db.sqlite3"):
        try:
            os.remove("./test_db.sqlite3")
        except FileNotFoundError:
            pass


@pytest.fixture(autouse=True)
def _override_dependencies(monkeypatch):
    # Override DB dependency
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides = {}


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture()
def create_user_in_db() -> callable:
    def _create(db, email="user@example.com", password_hash="hashed", full_name="Test User"):
        u = models.User(email=email, full_name=full_name, hashed_password=password_hash, is_active=True)
        db.add(u)
        db.commit()
        db.refresh(u)
        return u

    return _create


@pytest.fixture()
def auth_headers_token(client) -> dict:
    # Helper to register and login to get token using real endpoints
    signup_payload = {"email": "test@example.com", "password": "password123", "full_name": "Test"}
    # ensure signup ok; if already exists ignore
    resp = client.post("/auth/signup", json=signup_payload)
    if resp.status_code not in (200, 400):
        raise AssertionError(
            f"Unexpected signup status: {resp.status_code}, body={resp.text}"
        )
    # Try login
    login_resp = client.post(
        "/auth/login",
        json={
            "email": signup_payload["email"],
            "password": signup_payload["password"],
        },
    )
    assert login_resp.status_code == 200, login_resp.text
    data = login_resp.json()
    token = data.get("access_token") or data.get("token")
    assert token, "No token returned from login"
    return {"Authorization": f"Bearer {token}"}
