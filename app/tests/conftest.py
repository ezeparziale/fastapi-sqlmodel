import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings
from app.db.database import get_session
from app.main import app


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(settings.SQLALCHEMY_TEST_DATABASE_URI)

    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(autocommit=False, autoflush=False, bind=engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def test_team_1(client):
    json = {"name": "Justice League", "headquarters": "DC comics"}
    response = client.post("/api/v1/teams/", json=json)
    new_team = response.json()

    assert response.status_code == 200
    assert new_team["name"] == json["name"]
    assert new_team["headquarters"] == json["headquarters"]
    assert new_team["id"] is not None
    return new_team


@pytest.fixture
def test_team_2(client):
    json = {"name": "Teens Titans", "headquarters": "DC comics"}
    response = client.post("/api/v1/teams/", json=json)
    new_team = response.json()

    assert response.status_code == 200
    assert new_team["name"] == json["name"]
    assert new_team["headquarters"] == json["headquarters"]
    assert new_team["id"] is not None
    return new_team