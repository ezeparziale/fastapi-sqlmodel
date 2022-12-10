from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models import Team


def test_read_teams(session: Session, client: TestClient, test_team_1, test_team_2):
    response = client.get("/api/v1/teams/")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["name"] == test_team_1["name"]
    assert data[0]["headquarters"] == test_team_1["headquarters"]
    assert data[0]["id"] == test_team_1["id"]
    assert data[1]["name"] == test_team_2["name"]
    assert data[1]["headquarters"] == test_team_2["headquarters"]
    assert data[1]["id"] == test_team_2["id"]


def test_create_team(client: TestClient):
    response = client.post(
        "/api/v1/teams/", json={"name": "Justice League", "headquarters": "DC comics"}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Justice League"
    assert data["headquarters"] == "DC comics"
    assert data["id"] is not None


def test_create_team_incomplete(client: TestClient):
    # No headquarters
    response = client.post("/api/v1/teams/", json={"name": "Justice League"})
    assert response.status_code == 422


def test_create_team_invalid(client: TestClient):
    # headquarters has an invalid type
    response = client.post(
        "/api/v1/teams/",
        json={
            "name": "Justice League",
            "headquarters": {"message": "Invalid data type"},
        },
    )
    assert response.status_code == 422


def test_read_team(session: Session, client: TestClient, test_team_1):
    response = client.get(f"/api/v1/teams/{test_team_1['id']}")
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == test_team_1["name"]
    assert data["headquarters"] == test_team_1["headquarters"]
    assert data["id"] == test_team_1["id"]


def test_update_team(session: Session, client: TestClient, test_team_1):
    response = client.patch(
        f"/api/v1/teams/{test_team_1['id']}", json={"name": "Justice League 2"}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Justice League 2"
    assert data["headquarters"] == test_team_1["headquarters"]
    assert data["id"] == test_team_1["id"]


def test_delete_team(session: Session, client: TestClient, test_team_1):
    response = client.delete(f"/api/v1/teams/{test_team_1['id']}")

    team_in_db = session.get(Team, test_team_1["id"])

    assert response.status_code == 200
    assert team_in_db is None
