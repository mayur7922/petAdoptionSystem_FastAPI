from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from .main import app
from .database import get_db, Base
from .token import create_access_token
import pytest

client = TestClient(app)
SQLALCHEMY_DATABASE_URL = 'sqlite:///./test.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def override_get_db():
    database = TestingSessionLocal()
    try:
        yield database
    finally:
        database.close()

app.dependency_overrides[get_db] = override_get_db

# Testing admin routes

@pytest.fixture
def getAdminToken():
    access_token = create_access_token(data={"id": 1, "email": "admin", "role": "admin"})
    return access_token

def test_view_all_pets(getAdminToken):
    token = getAdminToken
    headers = {'Authorization': f'Bearer {token}'}

    response = client.get("/admin/pets", headers=headers)

    assert response.status_code == 200, response.text
    items = response.json()

    for data in items:
        assert data["type"]
        assert data["breed"]
        assert data["age"]


def test_create_new_pet(getAdminToken):
    token = getAdminToken
    headers = {'Authorization': f'Bearer {token}'}

    response = client.post(
        "/admin/pets/", json={"type": "Dog", "breed" : "b", "age": 10, "isAdopted":False, "user_id": 0},
        headers=headers
    )

    assert response.status_code == 201, response.text
    data = response.json()
    assert data["type"] == "Dog"
    assert data["breed"] == "b"
    assert data["age"] == 10
    assert data["isAdopted"] == False
    assert data["user_id"] == 0

def test_create_user():
    response = client.post(
        "/register/", json={"name": "user5", "email": "user5", "password": "user5"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "user5"
    assert data["email"] == "user5"
    assert data["role"] == "user"

def setup() -> None:
    Base.metadata.create_all(bind=engine)


def teardown() -> None:
    Base.metadata.drop_all(bind=engine)