from fastapi import FastAPI

# ==================================
# Import Models (IMPORTANT)
# ==================================

from app.models.user import User
from app.models.office import Office
from app.models.employee_office import EmployeeOffice
from app.models.attendance import Attendance

# ==================================
# Import Routes
# ==================================

from app.routes.auth import (
    router as auth_router
)

from app.routes.test_db import (
    router as test_db_router
)

from app.routes.attendance import (
    router as attendance_router
)

from app.routes.admin_office import (
    router as admin_office_router
)

from app.routes.admin_assignment import (
    router as admin_assignment_router
)

# ==================================
# FastAPI App
# ==================================

app = FastAPI(
    title="Attendance System",
    version="1.0.0"
)

# ==================================
# Home Route
# ==================================

@app.get("/")
def home():

    return {

        "status": True,

        "message": "Attendance API Running"

    }


# ==================================
# Database Test Route
# ==================================

app.include_router(
    test_db_router
)

# ==================================
# Authentication Routes
# ==================================

app.include_router(
    auth_router
)

# ==================================
# Attendance Routes
# ==================================

app.include_router(
    attendance_router
)

# ==================================
# Admin Office Routes
# ==================================

app.include_router(
    admin_office_router
)

# ==================================
# Admin Assignment Routes
# ==================================

app.include_router(
    admin_assignment_router
)