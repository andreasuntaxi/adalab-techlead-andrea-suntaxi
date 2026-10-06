import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DATABASE = os.getenv("DATABASE", "ada_exam")
REPORT_TOKEN = os.getenv("REPORT_TOKEN", "demo-only-not-a-real-secret")
DASHBOARD_ORIGIN = os.getenv("DASHBOARD_ORIGIN", "http://127.0.0.1:4200")