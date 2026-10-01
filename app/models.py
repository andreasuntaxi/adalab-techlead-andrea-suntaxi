from pydantic import BaseModel

class ProjectCreate(BaseModel):
    name: str
    budget: float
    status: str = "active"

class ProjectResponse(BaseModel):
    id: str
    name: str
    budget: str
    status: str

class ActivityCreate(BaseModel):
    title: str
    hours: float
    completed: bool = False
