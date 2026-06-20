import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import create_app

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    app = create_app()

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)


def test_register_rejects_non_petasight(client):
    res = client.post("/auth/register", json={"email": "user@gmail.com", "password": "secret1"})
    assert res.status_code == 403


def test_register_and_login_petasight(client):
    res = client.post(
        "/auth/register",
        json={"email": "user@petasight.com", "password": "secret1"},
    )
    assert res.status_code == 201

    res = client.post(
        "/auth/login",
        json={"email": "user@petasight.com", "password": "secret1"},
    )
    assert res.status_code == 200
    assert "access_token" in res.json()


def test_chat_requires_auth(client):
    res = client.post("/chat", json={"message": "hello"})
    assert res.status_code == 401


def test_chat_rejects_empty_message(client):
    client.post("/auth/register", json={"email": "user@petasight.com", "password": "secret1"})
    login = client.post("/auth/login", json={"email": "user@petasight.com", "password": "secret1"})
    token = login.json()["access_token"]

    res = client.post(
        "/chat",
        json={"message": "   "},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 422
#test cases