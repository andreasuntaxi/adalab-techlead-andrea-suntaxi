from bson import ObjectId
from app.database import get_db

def seed(db):
    # Idempotent fixture; preserves other records.
    for identifier, name, budget in [
        ("64b000000000000000000001", "SAT", 15000.0),
        ("64b000000000000000000002", "Chatbots", 8000.0),
    ]:
        db.projects.update_one({"_id": ObjectId(identifier)}, {"$set": {
            "name": name, "budget": budget, "status": "active"}}, upsert=True)
    for suffix, title, hours, completed in [
        (1, "API", 10.0, True), (2, "Dashboard", 20.0, False),
        (3, "Tests", 5.0, True),
    ]:
        db.activities.update_one({"_id": ObjectId(f"65b{suffix:021x}")},
            {"$set": {"project_id": "64b000000000000000000001", "title": title,
                       "hours": hours, "completed": completed}}, upsert=True)

if __name__ == "__main__":
    seed(get_db())
    print("Fixture loaded")
