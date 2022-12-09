import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.main import app
from app.db.database import get_session

from app.core.config import settings

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