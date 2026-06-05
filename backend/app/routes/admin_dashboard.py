from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy import func
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

    prefix="/admin/dashboard",

    tags=["Dashboard"]

)


# ==========================================
# DASHBOARD SUMMARY
# ==========================================

@router.get("/summary")
def dashboard_summary(

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

    total_employees = db.query(
        User
    ).filter(
        User.role == "employee"
    ).count()

    active_employees = db.query(
        User
    ).filter(

        User.role == "employee",

        User.is_active == True

    ).count()

    inactive_employees = db.query(
        User
    ).filter(

        User.role == "employee",

        User.is_active == False

    ).count()

    total_offices = db.query(
        Office
    ).filter(
        Office.is_active == True
    ).count()

    present_today = db.query(
        Attendance
    ).filter(

        Attendance.attendance_date
        ==
        date.today()

    ).count()

    checked_out = db.query(
        Attendance
    ).filter(

        Attendance.attendance_date
        ==
        date.today(),

        Attendance.check_out
        !=
        None

    ).count()

    checked_in = present_today - checked_out

    absent_today = (
        active_employees
        -
        present_today
    )

    return {

        "status": True,

        "data": {

            "total_employees":
            total_employees,

            "active_employees":
            active_employees,

            "inactive_employees":
            inactive_employees,

            "total_offices":
            total_offices,

            "present_today":
            present_today,

            "absent_today":
            absent_today,

            "checked_in":
            checked_in,

            "checked_out":
            checked_out

        }

    }
    
# ==========================================
# TODAY ATTENDANCE
# ==========================================

@router.get("/today-attendance")
def today_attendance(

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
    
# ==========================================
# PRESENT EMPLOYEES
# ==========================================

@router.get("/present")
def present_employees(

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

    present_count = db.query(
        Attendance
    ).filter(

        Attendance.attendance_date
        ==
        date.today()

    ).count()

    return {

        "status": True,

        "present":
        present_count

    }
    
@router.get("/absent")
def absent_employees(

    current_user=Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )

):

    active = db.query(
        User
    ).filter(

        User.role == "employee",

        User.is_active == True

    ).count()

    present = db.query(
        Attendance
    ).filter(

        Attendance.attendance_date
        ==
        date.today()

    ).count()

    return {

        "status": True,

        "absent":
        active - present

    }
    
@router.get("/office-wise")
def office_wise(

    current_user=Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )

):

    offices = db.query(
        Office
    ).all()

    result = []

    for office in offices:

        total = db.query(
            Attendance
        ).filter(

            Attendance.office_id
            ==
            office.id,

            Attendance.attendance_date
            ==
            date.today()

        ).count()

        result.append({

            "office":
            office.office_name,

            "present":
            total

        })

    return {

        "status": True,

        "data":
        result

    }
    
@router.get("/departments")
def department_summary(

    current_user=Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )

):

    departments = db.query(
        User.department
    ).distinct().all()

    data = []

    for dep in departments:

        total = db.query(
            User
        ).filter(

            User.department
            ==
            dep[0]

        ).count()

        data.append({

            "department":
            dep[0],

            "count":
            total

        })

    return {

        "status": True,

        "data":
        data

    }
    
    
# ==========================================
# RECENT CHECK-INS
# ==========================================

@router.get("/recent-checkins")
def recent_checkins(

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

        Attendance.check_in
        !=
        None

    ).order_by(

        Attendance.check_in.desc()

    ).limit(5).all()

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
            row.check_in

        })

    return {

        "status": True,

        "count":
        len(data),

        "data":
        data

    }
    
# ==========================================
# DASHBOARD STATS
# ==========================================

@router.get("/stats")
def dashboard_stats(

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

    total_employees = db.query(
        User
    ).filter(

        User.role == "employee",

        User.is_active == True

    ).count()

    present_today = db.query(
        Attendance
    ).filter(

        Attendance.attendance_date
        ==
        date.today()

    ).count()

    total_offices = db.query(
        Office
    ).filter(

        Office.is_active == True

    ).count()

    offices_used = db.query(
        Attendance.office_id
    ).filter(

        Attendance.attendance_date
        ==
        date.today()

    ).distinct().count()

    avg_hours = db.query(
        func.avg(
            Attendance.work_hours
        )
    ).scalar()

    if avg_hours is None:

        avg_hours = 0

    attendance_percentage = 0

    if total_employees > 0:

        attendance_percentage = round(

            (
                present_today
                /
                total_employees
            ) * 100,

            2

        )

    office_utilization = 0

    if total_offices > 0:

        office_utilization = round(

            (
                offices_used
                /
                total_offices
            ) * 100,

            2

        )

    return {

        "status": True,

        "data": {

            "attendance_percentage":
            attendance_percentage,

            "office_utilization":
            office_utilization,

            "average_work_hours":
            round(
                float(avg_hours),
                2
            )

        }

    }
