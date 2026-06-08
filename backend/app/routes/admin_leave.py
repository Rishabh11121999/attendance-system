from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.db import get_db

from app.utils.auth_middleware import (
    get_current_user
)

from app.models.leave_request import (
    LeaveRequest
)

from app.models.user import (
    User
)

from app.schemas.leave_schema import (
    LeaveAction
)

from datetime import date


router = APIRouter(

    prefix="/admin/leaves",

    tags=["Leave Management"]

)


# ==========================================
# ALL LEAVES
# ==========================================

@router.get("/list")
def leave_list(

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
        LeaveRequest
    ).order_by(

        LeaveRequest.created_at.desc()

    ).all()

    data = []

    for row in records:

        employee = db.query(
            User
        ).filter(

            User.id == row.user_id

        ).first()

        data.append({

            "leave_id":
            row.id,

            "employee_id":
            row.user_id,

            "employee_name":
            employee.name if employee else None,

            "employee_code":
            employee.employee_code if employee else None,

            "leave_type":
            row.leave_type,

            "from_date":
            row.from_date,

            "to_date":
            row.to_date,

            "total_days":
            row.total_days,

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
# PENDING LEAVES
# ==========================================

@router.get("/pending")
def pending_leaves(

    current_user=Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )

):

    return get_status_data(
        "Pending",
        current_user,
        db
    )


# ==========================================
# APPROVED LEAVES
# ==========================================

@router.get("/approved")
def approved_leaves(

    current_user=Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )

):

    return get_status_data(
        "Approved",
        current_user,
        db
    )


# ==========================================
# REJECTED LEAVES
# ==========================================

@router.get("/rejected")
def rejected_leaves(

    current_user=Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )

):

    return get_status_data(
        "Rejected",
        current_user,
        db
    )


# ==========================================
# CANCELLED LEAVES
# ==========================================

@router.get("/cancelled")
def cancelled_leaves(

    current_user=Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )

):

    return get_status_data(
        "Cancelled",
        current_user,
        db
    )


# ==========================================
# COMMON STATUS FUNCTION
# ==========================================

def get_status_data(

    status_name,

    current_user,

    db

):

    if current_user["role"] != "admin":

        return {

            "status": False,

            "message":
            "Only admin allowed."

        }

    records = db.query(
        LeaveRequest
    ).filter(

        LeaveRequest.status
        ==
        status_name

    ).all()

    data = []

    for row in records:

        employee = db.query(
            User
        ).filter(

            User.id == row.user_id

        ).first()

        data.append({

            "leave_id":
            row.id,

            "employee_name":
            employee.name if employee else None,

            "employee_code":
            employee.employee_code if employee else None,

            "leave_type":
            row.leave_type,

            "from_date":
            row.from_date,

            "to_date":
            row.to_date,

            "total_days":
            row.total_days

        })

    return {

        "status": True,

        "count":
        len(data),

        "data":
        data

    }


# ==========================================
# APPROVE LEAVE
# ==========================================

@router.put("/approve/{leave_id}")
def approve_leave(

    leave_id: int,

    payload: LeaveAction,

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

    leave = db.query(
        LeaveRequest
    ).filter(

        LeaveRequest.id
        ==
        leave_id

    ).first()

    if not leave:

        return {

            "status": False,

            "message":
            "Leave not found."

        }

    if leave.status != "Pending":

        return {

            "status": False,

            "message":
            "Only pending leave can be approved."

        }

    leave.status = "Approved"

    leave.approved_by = current_user["id"]

    leave.admin_remarks = payload.admin_remarks

    db.commit()

    db.refresh(
        leave
    )

    return {

        "status": True,

        "message":
        "Leave approved successfully."

    }


# ==========================================
# REJECT LEAVE
# ==========================================

@router.put("/reject/{leave_id}")
def reject_leave(

    leave_id: int,

    payload: LeaveAction,

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

    leave = db.query(
        LeaveRequest
    ).filter(

        LeaveRequest.id
        ==
        leave_id

    ).first()

    if not leave:

        return {

            "status": False,

            "message":
            "Leave not found."

        }

    if leave.status != "Pending":

        return {

            "status": False,

            "message":
            "Only pending leave can be rejected."

        }

    leave.status = "Rejected"

    leave.approved_by = current_user["id"]

    leave.admin_remarks = payload.admin_remarks

    db.commit()

    db.refresh(
        leave
    )

    return {

        "status": True,

        "message":
        "Leave rejected successfully."

    }


# ==========================================
# LEAVE DASHBOARD STATS
# ==========================================

@router.get("/stats")
def leave_stats(

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

    pending = db.query(
        LeaveRequest
    ).filter(
        LeaveRequest.status == "Pending"
    ).count()

    approved = db.query(
        LeaveRequest
    ).filter(
        LeaveRequest.status == "Approved"
    ).count()

    rejected = db.query(
        LeaveRequest
    ).filter(
        LeaveRequest.status == "Rejected"
    ).count()

    cancelled = db.query(
        LeaveRequest
    ).filter(
        LeaveRequest.status == "Cancelled"
    ).count()

    today_leave = db.query(
        LeaveRequest
    ).filter(

        LeaveRequest.status
        ==
        "Approved",

        LeaveRequest.from_date
        <=
        date.today(),

        LeaveRequest.to_date
        >=
        date.today()

    ).count()

    return {

        "status": True,

        "data": {

            "pending":
            pending,

            "approved":
            approved,

            "rejected":
            rejected,

            "cancelled":
            cancelled,

            "today_on_leave":
            today_leave

        }

    }
    
# ==========================================
# LEAVE DETAILS
# ==========================================

@router.get("/{leave_id}")
def leave_details(

    leave_id: int,

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

    leave = db.query(
        LeaveRequest
    ).filter(

        LeaveRequest.id == leave_id

    ).first()

    if not leave:

        return {

            "status": False,

            "message":
            "Leave not found."

        }

    employee = db.query(
        User
    ).filter(

        User.id == leave.user_id

    ).first()

    return {

        "status": True,

        "data": {

            "leave_id":
            leave.id,

            "employee_id":
            leave.user_id,

            "employee_name":
            employee.name if employee else None,

            "employee_code":
            employee.employee_code if employee else None,

            "leave_type":
            leave.leave_type,

            "from_date":
            leave.from_date,

            "to_date":
            leave.to_date,

            "total_days":
            leave.total_days,

            "reason":
            leave.reason,

            "status":
            leave.status,

            "admin_remarks":
            leave.admin_remarks,

            "approved_by":
            leave.approved_by

        }

    }
   