import os
import pandas as pd

from fastapi.responses import FileResponse


from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from sqlalchemy.orm import Session

from datetime import date

from app.database.db import get_db

from app.utils.auth_middleware import (
    get_current_user
)

from app.models.user import User    
from app.models.office import Office
from app.models.attendance import Attendance

router = APIRouter(

    prefix="/admin/reports",

    tags=["Reports"]

)


# ==========================================
# DAILY REPORT
# ==========================================

@router.get("/daily")
def daily_report(

    current_user=Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )

):

    if current_user["role"] != "admin":

        return {

            "status": False,

            "message":
            "Only admin allowed."

        }

    records = db.query(
        Attendance
    ).filter(

        Attendance.attendance_date
        ==
        date.today()

    ).all()

    data = []

    for row in records:

        employee = db.query(
            User
        ).filter(
            User.id == row.user_id
        ).first()

        office = db.query(
            Office
        ).filter(
            Office.id == row.office_id
        ).first()

        data.append({

            "employee_code":
            employee.employee_code,

            "name":
            employee.name,

            "office":
            office.office_name,

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

        "date":
        date.today(),

        "count":
        len(data),

        "data":
        data

    }


# ==========================================
# MONTHLY REPORT
# ==========================================

@router.get("/monthly")
def monthly_report(

    year: int = Query(...),

    month: int = Query(...),

    current_user=Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )

):

    if current_user["role"] != "admin":

        return {

            "status": False,

            "message":
            "Only admin allowed."

        }

    records = db.query(
        Attendance
    ).all()

    data = []

    for row in records:

        if (

            row.attendance_date.year == year

            and

            row.attendance_date.month == month

        ):

            employee = db.query(
                User
            ).filter(
                User.id == row.user_id
            ).first()

            office = db.query(
                Office
            ).filter(
                Office.id == row.office_id
            ).first()

            data.append({

                "employee_code":
                employee.employee_code,

                "name":
                employee.name,

                "office":
                office.office_name,

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

        "year":
        year,

        "month":
        month,

        "count":
        len(data),

        "data":
        data

    }


# ==========================================
# EMPLOYEE REPORT
# ==========================================

@router.get("/employee/{user_id}")
def employee_report(

    user_id: int,

    current_user=Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )

):

    if current_user["role"] != "admin":

        return {

            "status": False,

            "message":
            "Only admin allowed."

        }

    employee = db.query(
        User
    ).filter(
        User.id == user_id
    ).first()

    if not employee:

        return {

            "status": False,

            "message":
            "Employee not found."

        }

    records = db.query(
        Attendance
    ).filter(
        Attendance.user_id == user_id
    ).all()

    data = []

    for row in records:

        office = db.query(
            Office
        ).filter(
            Office.id == row.office_id
        ).first()

        data.append({

            "office":
            office.office_name,

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

        "employee": {

            "id":
            employee.id,

            "employee_code":
            employee.employee_code,

            "name":
            employee.name

        },

        "attendance":
        data

    }


# ==========================================
# OFFICE REPORT
# ==========================================

@router.get("/office/{office_id}")
def office_report(

    office_id: int,

    current_user=Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )

):

    if current_user["role"] != "admin":

        return {

            "status": False,

            "message":
            "Only admin allowed."

        }

    office = db.query(
        Office
    ).filter(
        Office.id == office_id
    ).first()

    if not office:

        return {

            "status": False,

            "message":
            "Office not found."

        }

    records = db.query(
        Attendance
    ).filter(
        Attendance.office_id == office_id
    ).all()

    data = []

    for row in records:

        employee = db.query(
            User
        ).filter(
            User.id == row.user_id
        ).first()

        data.append({

            "employee_code":
            employee.employee_code,

            "name":
            employee.name,

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

        "office":
        office.office_name,

        "count":
        len(data),

        "employees":
        data

    }


# ==========================================
# CSV EXPORT
# ==========================================

@router.get("/export/csv")
def export_csv(

    current_user=Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )

):

    if current_user["role"] != "admin":

        return {

            "status": False,

            "message":
            "Only admin allowed."

        }

    records = db.query(
        Attendance
    ).all()

    data = []

    for row in records:

        employee = db.query(
            User
        ).filter(
            User.id == row.user_id
        ).first()

        office = db.query(
            Office
        ).filter(
            Office.id == row.office_id
        ).first()

        data.append({

            "Employee Code":
            employee.employee_code,

            "Name":
            employee.name,

            "Office":
            office.office_name,

            "Attendance Date":
            row.attendance_date,

            "Check In":
            row.check_in,

            "Check Out":
            row.check_out,

            "Work Hours":
            float(row.work_hours),

            "Status":
            row.status

        })

    df = pd.DataFrame(data)

    file_path = "attendance_report.csv"

    df.to_csv(
        file_path,
        index=False
    )

    return FileResponse(

        path=file_path,

        filename="attendance_report.csv",

        media_type="text/csv"

    )




# ==========================================
# EXCEL EXPORT
# ==========================================

@router.get("/export/excel")
def export_excel(

    current_user=Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )

):

    if current_user["role"] != "admin":

        return {

            "status": False,

            "message":
            "Only admin allowed."

        }

    records = db.query(
        Attendance
    ).all()

    data = []

    for row in records:

        employee = db.query(
            User
        ).filter(
            User.id == row.user_id
        ).first()

        office = db.query(
            Office
        ).filter(
            Office.id == row.office_id
        ).first()

        data.append({

            "Employee Code":
            employee.employee_code,

            "Name":
            employee.name,

            "Office":
            office.office_name,

            "Attendance Date":
            row.attendance_date,

            "Check In":
            row.check_in,

            "Check Out":
            row.check_out,

            "Work Hours":
            float(row.work_hours),

            "Status":
            row.status

        })

    df = pd.DataFrame(data)

    file_path = "attendance_report.xlsx"

    df.to_excel(
        file_path,
        index=False
    )

    return FileResponse(

        path=file_path,

        filename="attendance_report.xlsx",

        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    )


