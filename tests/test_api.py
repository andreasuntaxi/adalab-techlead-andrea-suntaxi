import pytest

ID = "64b000000000000000000001"
EMPTY = "64b000000000000000000002"
MISSING = "64b000000000000000000099"

def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}

def test_list(client):
    response = client.get("/projects")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_summary(client):
    response = client.get(f"/projects/{ID}/summary")
    assert response.status_code == 200
    assert response.json() == {"project_id": ID, "name": "SAT", "activity_count": 3,
        "completed_count": 2, "total_hours": 35.0, "completion_rate": pytest.approx(2/3)}

def test_missing_summary(client):
    assert client.get(f"/projects/{MISSING}/summary").status_code == 404

def test_empty_summary(client):
    response = client.get(f"/projects/{EMPTY}/summary")
    assert response.status_code == 200
    assert response.json() == {"project_id": EMPTY, "name": "Chatbots", "activity_count": 0,
        "completed_count": 0, "total_hours": 0, "completion_rate": 0}

def test_invalid_id(client):
    assert client.get("/projects/not-an-id/summary").status_code == 422
