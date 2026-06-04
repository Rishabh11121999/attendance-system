from fastapi import APIRouter
from sqlalchemy import text
from app.database.db import SessionLocal

router = APIRouter()

@router.get("/test-db")
def test_db():

    db = SessionLocal()

    result = db.execute(
        text("SELECT 1")
    )

    return {
        "message": "Database Connected"
    }