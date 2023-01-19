from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models import Hero


def test_read_heroes(session: Session, client: TestClient, test_hero_1, test_hero_2):
    response = client.get("/api/v1/heros/")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["name"] == test_hero_1["name"]
    assert data[0]["secret_name"] == test_hero_1["secret_name"]
    assert data[0]["age"] == test_hero_1["age"]
    assert data[0]["id"] == test_hero_1["id"]
    assert data[0]["team_id"] == test_hero_1["team_id"]
    assert data[1]["name"] == test_hero_2["name"]
    assert data[1]["secret_name"] == test_hero_2["secret_name"]
    assert data[1]["age"] == test_hero_2["age"]
    assert data[1]["id"] == test_hero_2["id"]
    assert data[1]["team_id"] == test_hero_1["team_id"]


def test_create_hero(client: TestClient):
    response = client.post(
        "/api/v1/heros/",
        json={"name": "Green Lantern", "secret_name": "Hal Jordan", "age": 50},
    )  # nosec B106
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Green Lantern"
    assert data["secret_name"] == "Hal Jordan"
    assert data["age"] == 50
    assert data["id"] is not None


def test_create_hero_incomplete(client: TestClient):
    # No secret_name
    response = client.post("/api/v1/heros/", json={"name": "Batman"})
    assert response.status_code == 422


def test_create_hero_invalid(client: TestClient):
    # secret_name has an invalid type
    response = client.post(
        "/api/v1/heros/",
        json={
            "name": "Batman",
            "secret_name": {"message": "Do you wanna know my secret identity?"},
        },
    )
    assert response.status_code == 422


def test_read_hero(session: Session, client: TestClient, test_hero_1):
    response = client.get(f"/api/v1/heros/{test_hero_1['id']}")
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == test_hero_1["name"]
    assert data["secret_name"] == test_hero_1["secret_name"]
    assert data["age"] == test_hero_1["age"]
    assert data["id"] == test_hero_1["id"]


def test_update_hero(session: Session, client: TestClient):
    hero_1 = Hero(name="Flash", secret_name="Jay Garrick")  # nosec B106
    session.add(hero_1)
    session.commit()

    response = client.patch(
        f"/api/v1/heros/{hero_1.id}", json={"secret_name": "Barry Allen"}
    )  # nosec B106
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Flash"
    assert data["secret_name"] == "Barry Allen"
    assert data["age"] is None
    assert data["id"] == hero_1.id


def test_delete_hero(session: Session, client: TestClient, test_hero_2):
    response = client.delete(f"/api/v1/heros/{test_hero_2['id']}")
    hero_in_db = session.get(Hero, test_hero_2["id"])

    assert response.status_code == 200
    assert hero_in_db is None
