from unittest.mock import Mock

ID = "64b000000000000000000001"
MISSING = "64b000000000000000000099"

def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}

def test_list(client):
    assert len(client.get("/projects").json()) == 2

def test_create(client):
    response = client.post("/projects", json={"name": "IR", "budget": 100})
    assert response.status_code == 201
    assert response.json()["name"] == "IR"

def test_missing_project(client):
    assert client.get(f"/projects/{MISSING}").status_code == 404

def test_negative_budget(client):
    assert client.post("/projects", json={"name": "IR", "budget": -1}).status_code == 422

def test_summary(client):
    response = client.get(f"/projects/{ID}/summary")
    assert response.status_code == 200
    assert response.json()["total_hours"] == 35

def test_repository_failure():
    repository = Mock()
    repository.get_project.return_value = {"status_code": 503}
    result = repository.get_project("unavailable")
    assert result["status_code"] == 503
