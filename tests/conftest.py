import pytest
import mongomock
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from scripts.seed import seed

@pytest.fixture
def db():
    database = mongomock.MongoClient().ada_exam
    seed(database)
    return database

@pytest.fixture
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as value:
        yield value
    app.dependency_overrides.clear()
