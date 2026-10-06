import pytest

ID = "64b000000000000000000001"
EMPTY = "64b000000000000000000002"
MISSING = "64b000000000000000000099"

def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}

def test_list(client, db):
    db.projects.update_many(
        {},
        {"$set": {"metadata": {"source": "internal"}, "created_by": "team"}},
    )

    response = client.get("/projects")

    assert response.status_code == 200
    projects = response.json()
    assert len(projects) == 2

    for project in projects:
        assert set(project) == {"id", "name", "budget", "status"}
        assert isinstance(project["id"], str)
        assert type(project["budget"]) in (int, float)

    by_id = {project["id"]: project for project in projects}
    assert by_id == {
        ID: {
            "id": ID,
            "name": "SAT",
            "budget": 15000.0,
            "status": "active",
        },
        EMPTY: {
            "id": EMPTY,
            "name": "Chatbots",
            "budget": 8000.0,
            "status": "active",
        },
    }

def test_empty_list(client, db):
    db.projects.delete_many({})

    response = client.get("/projects")

    assert response.status_code == 200
    assert response.json() == []

def test_summary(client, db):
    db.activities.insert_one({
        "project_id": EMPTY,
        "title": "Actividad de otro proyecto",
        "hours": 100.0,
        "completed": True,
    })

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
