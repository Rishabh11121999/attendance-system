from fastapi import FastAPI

from app.routes.auth import (
    router as auth_router
)

app = FastAPI(
    title="Attendance System",
    version="1.0.0"
)

app.include_router(
    auth_router
)

@app.get("/")
def home():

    return {

        "status": True,

        "message":
        "Attendance API Running"

    }