from fastapi import FastAPI

app = FastAPI(
    title="Attendance System",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "status": True,
        "message": "Attendance API Running Successfully"
    }