import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app
from routers.auth import get_current_user

#i have created different db for test purpose
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# clean test database before running tests
@pytest.fixture(scope="session", autouse=True)
def clean_test_db():
    """Delete the test database file before running tests."""
    db_path = "./test.db"
    if os.path.exists(db_path):
        os.remove(db_path)

# dependency override to use the test database
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# mock authentication to simulate a logged-in user
def override_get_current_user():
    return {"user_id": 1, "user_role": "manager"}

# applying dependency overrides
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

@pytest.fixture(scope="module")
def client():
    """Creates the database and test client."""
    Base.metadata.create_all(bind=engine)  # Create tables for the test database
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)  # Cleanup after tests

@pytest.fixture
def db():
    """Provides a fresh database session for each test."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
