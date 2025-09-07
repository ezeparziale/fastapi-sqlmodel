import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings
from app.db.database import get_db
from app.main import app


@pytest.fixture(name="session", scope="session")
def session_fixture():
    engine = create_engine(settings.SQLALCHEMY_TEST_DATABASE_URI.unicode_string())

    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(autocommit=False, autoflush=False, bind=engine) as session:
        yield session


@pytest.fixture(name="client", scope="session")
def client_fixture(session: Session):
    def get_db_override():
        return session

    app.dependency_overrides[get_db] = get_db_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(scope="session", autouse=True)
def test_team_1(client):
    json = {"name": "Justice League", "headquarters": "DC comics"}
    response = client.post("/api/v1/teams/", json=json)
    new_team = response.json()

    assert response.status_code == 200
    assert new_team["name"] == json["name"]
    assert new_team["headquarters"] == json["headquarters"]
    assert new_team["id"] is not None
    return new_team


@pytest.fixture(scope="session", autouse=True)
def test_team_2(client):
    json = {"name": "Teens Titans", "headquarters": "DC comics"}
    response = client.post("/api/v1/teams/", json=json)
    new_team = response.json()

    assert response.status_code == 200
    assert new_team["name"] == json["name"]
    assert new_team["headquarters"] == json["headquarters"]
    assert new_team["id"] is not None
    return new_team


@pytest.fixture(scope="session", autouse=True)
def test_hero_1(client, test_team_1):
    json = {
        "name": "Batman",
        "secret_name": "Bruce Wayne",
        "team_id": test_team_1["id"],
    }
    response = client.post("/api/v1/heros/", json=json)
    new_hero = response.json()

    assert response.status_code == 200
    assert new_hero["name"] == json["name"]
    assert new_hero["secret_name"] == json["secret_name"]
    assert new_hero["id"] is not None
    return new_hero


@pytest.fixture(scope="session", autouse=True)
def test_hero_2(client, test_team_1):
    json = {
        "name": "Superman",
        "secret_name": "Clark Kent",
        "age": 43,
        "team_id": test_team_1["id"],
    }
    response = client.post("/api/v1/heros/", json=json)
    new_hero = response.json()

    assert response.status_code == 200
    assert new_hero["name"] == json["name"]
    assert new_hero["secret_name"] == json["secret_name"]
    assert new_hero["age"] == json["age"]
    assert new_hero["id"] is not None
    return new_hero
