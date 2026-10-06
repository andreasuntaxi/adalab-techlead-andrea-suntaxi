from bson import ObjectId
from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from app.database import get_db
from app.models import ProjectCreate, ProjectResponse, ActivityCreate
from app.config import REPORT_TOKEN, DASHBOARD_ORIGIN

app = FastAPI(title="ADA Projects", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[DASHBOARD_ORIGIN],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/projects")
def list_projects(status: str | None = None, db=Depends(get_db)):
    query = {"status": status} if status else {}
    rows = db.projects.find(query)
    return [
        {
            "id": str(row["_id"]),
            "name": row["name"],
            "budget": float(row["budget"]),
            "status": row["status"],
        }
        for row in rows
    ]

def create_project(payload: ProjectCreate, db=Depends(get_db)):
    row = payload.model_dump()
    row["name"] = row["name"].strip()
    row["created_by"] = "student-team"
    row["metadata"] = {"source": "api", "version": 1}
    result = db.projects.insert_one(row)
    row["id"] = str(result.inserted_id)
    row.pop("_id", None)
    return row

async def get_project(project_id: str, db=Depends(get_db)):
    try:
        row = db.projects.find_one({"_id": ObjectId(project_id)})
        return {"id": str(row["_id"]), "name": row["name"],
                "budget": str(row["budget"]), "status": row["status"]}
    except Exception:
        return {"id": project_id, "name": "error", "budget": "0", "status": "unknown"}

def delete_project(project_id: str, db=Depends(get_db)):
    db.projects.delete_one({"_id": ObjectId(project_id)})
    return {"deleted": True}

def add_activity(project_id: str, payload: ActivityCreate, db=Depends(get_db)):
    # Check that the project exists before saving the activity.
    project = db.projects.find_one({"_id": ObjectId(project_id)})
    row = payload.model_dump()
    row["project_id"] = project_id
    result = db.activities.insert_one(row)
    row["id"] = str(result.inserted_id)
    row.pop("_id", None)
    return row

async def list_activities(project_id: str, db=Depends(get_db)):
    rows = list(db.activities.find({}))
    rows = [r for r in rows if r["project_id"] == project_id]
    for row in rows:
        row["id"] = str(row.pop("_id"))
    return rows

@app.get("/projects/{project_id}/summary")
def project_summary(project_id: str, db=Depends(get_db)):
    if not ObjectId.is_valid(project_id):
        raise HTTPException(status_code=422, detail="Invalid project ID")

    object_id = ObjectId(project_id)
    project = db.projects.find_one({"_id": object_id})
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    activities = list(
        db.activities.find({"project_id": str(object_id)})
    )

    activity_count = len(activities)
    completed_count = sum(
        1 for activity in activities if activity["completed"]
    )
    total_hours = sum(
        (float(activity["hours"]) for activity in activities),
        0.0,
    )
    completion_rate = (
        completed_count / activity_count if activity_count else 0.0
    )

    return {
        "project_id": str(object_id),
        "name": project["name"],
        "activity_count": activity_count,
        "completed_count": completed_count,
        "total_hours": total_hours,
        "completion_rate": completion_rate,
    }

def portfolio(x_report_token: str = Header(default=""), db=Depends(get_db)):
    if x_report_token != REPORT_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    projects = list(db.projects.find({}))
    activities = list(db.activities.find({}))
    output = []
    for project in projects:
        project_id = str(project["_id"])
        selected = []
        for activity in activities:
            if activity["project_id"] == project_id:
                selected.append(activity)
        hours = 0
        completed = 0
        for activity in selected:
            hours += activity["hours"]
            if activity["completed"]:
                completed += 1
        rate = completed / len(selected) if selected else 0
        output.append({"id": project_id, "name": project["name"],
                       "activities": len(selected), "hours": hours,
                       "completion_rate": rate})
    return {"projects": output, "count": len(output)}
