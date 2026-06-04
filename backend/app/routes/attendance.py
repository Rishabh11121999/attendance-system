from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from datetime import datetime
from datetime import date

from app.database.db import get_db

from app.schemas.attendance_schema import (
    CheckInRequest,
    CheckOutRequest
)

from app.utils.auth_middleware import (
    get_current_user
)

from app.models.attendance import Attendance
from app.models.office import Office
from app.models.employee_office import EmployeeOffice

from app.services.geo_service import GeoService

router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"]
)


# ==========================
# CHECK-IN
# ==========================

@router.post("/check-in")
def check_in(
    payload: CheckInRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    assignment = db.query(
        EmployeeOffice
    ).filter(
        EmployeeOffice.user_id == current_user["id"],
        EmployeeOffice.is_active == True
    ).first()

    if not assignment:

        return {
            "status": False,
            "message": "No office assigned."
        }

    office = db.query(
        Office
    ).filter(
        Office.id == assignment.office_id,
        Office.is_active == True
    ).first()

    if not office:

        return {
            "status": False,
            "message": "Office not found."
        }

    location = GeoService.is_inside_radius(

        office.latitude,
        office.longitude,

        payload.latitude,
        payload.longitude,

        office.radius

    )

    if not location["allowed"]:

        return {

            "status": False,

            "message": "You are outside office radius.",

            "distance":
            location["distance"]

        }

    already = db.query(
        Attendance
    ).filter(

        Attendance.user_id == current_user["id"],

        Attendance.attendance_date == date.today()

    ).first()

    if already:

        return {

            "status": False,

            "message":
            "Already checked in today."

        }

    attendance = Attendance(

        user_id=current_user["id"],

        office_id=office.id,

        attendance_date=date.today(),

        check_in=datetime.now(),

        latitude=payload.latitude,

        longitude=payload.longitude,

        status="Present"

    )

    db.add(attendance)

    db.commit()

    db.refresh(attendance)

    return {

        "status": True,

        "message":
        "Check-In Successful",

        "office":
        office.office_name,

        "distance":
        location["distance"],

        "check_in":
        attendance.check_in

    }


# ==========================
# CHECK-OUT
# ==========================

@router.post("/check-out")
def check_out(

    payload: CheckOutRequest,

    current_user=Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )

):

    attendance = db.query(
        Attendance
    ).filter(

        Attendance.user_id == current_user["id"],

        Attendance.attendance_date == date.today()

    ).first()

    if not attendance:

        return {

            "status": False,

            "message":
            "Please check in first."

        }

    if attendance.check_out:

        return {

            "status": False,

            "message":
            "Already checked out."

        }

    attendance.check_out = datetime.now()

    attendance.latitude = payload.latitude

    attendance.longitude = payload.longitude

    seconds = (

        attendance.check_out

        -

        attendance.check_in

    ).total_seconds()

    attendance.work_hours = round(

        seconds / 3600,

        2

    )

    db.commit()

    db.refresh(attendance)

    return {

        "status": True,

        "message":
        "Check-Out Successful",

        "work_hours":
        attendance.work_hours,

        "check_out":
        attendance.check_out

    }


# ==========================
# TODAY ATTENDANCE
# ==========================

@router.get("/today")
def today_attendance(

    current_user=Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )

):

    attendance = db.query(
        Attendance
    ).filter(

        Attendance.user_id == current_user["id"],

        Attendance.attendance_date == date.today()

    ).first()

    if not attendance:

        return {

            "status": False,

            "message":
            "No attendance found."

        }

    return {

        "status": True,

        "data": {

            "date":
            attendance.attendance_date,

            "check_in":
            attendance.check_in,

            "check_out":
            attendance.check_out,

            "work_hours":
            attendance.work_hours,

            "status":
            attendance.status

        }

    }


# ==========================
# ATTENDANCE HISTORY
# ==========================

@router.get("/history")
def attendance_history(

    current_user=Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )

):

    records = db.query(
        Attendance
    ).filter(

        Attendance.user_id == current_user["id"]

    ).order_by(

        Attendance.attendance_date.desc()

    ).all()

    data = []

    for row in records:

        data.append({

            "attendance_date":
            row.attendance_date,

            "check_in":
            row.check_in,

            "check_out":
            row.check_out,

            "work_hours":
            float(row.work_hours),

            "status":
            row.status

        })

    return {

        "status": True,

        "count":
        len(data),

        "data":
        data

    }