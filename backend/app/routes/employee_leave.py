from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from datetime import date

from app.database.db import get_db

from app.utils.auth_middleware import (
    get_current_user
)

from app.models.leave_request import (
    LeaveRequest
)

from app.schemas.leave_schema import (
    LeaveCreate
)

from app.models.user import (
    User
)

router = APIRouter(

    prefix="/employee/leaves",

    tags=["Employee Leave"]

)


# ==========================================
# APPLY LEAVE
# ==========================================

@router.post("/apply")
def apply_leave(

    payload: LeaveCreate,

    current_user=Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )

):

    if current_user["role"] != "employee":

        return {

            "status": False,

            "message":
            "Only employee can apply leave."

        }
        
    # Validate date range

    if payload.from_date > payload.to_date:

        return {

            "status": False,

            "message":
            "From date cannot be greater than To date."

        }

    # Validate past date

    if payload.from_date < date.today():

        return {

            "status": False,

            "message":
            "Past date leave cannot be applied."

        }


    
        
    overlap = db.query(
        LeaveRequest
    ).filter(

        LeaveRequest.user_id
        ==
        current_user["id"],

        LeaveRequest.status.in_(
            ["Pending", "Approved"]
        ),

        LeaveRequest.from_date
        <=
        payload.to_date,

        LeaveRequest.to_date
        >=
        payload.from_date

    ).first()

    if overlap:

        return {

            "status": False,

            "message":
            "Leave already exists for selected dates."

        }

    total_days = (

        payload.to_date
        -
        payload.from_date

    ).days + 1

    leave = LeaveRequest(

        user_id=current_user["id"],

        leave_type=payload.leave_type,

        from_date=payload.from_date,

        to_date=payload.to_date,

        total_days=total_days,

        reason=payload.reason,

        status="Pending"

    )

    try:

        db.add(
            leave
        )

        db.commit()

        db.refresh(
            leave
        )

    except Exception as e:

        db.rollback()

        return {

            "status": False,

            "message":
            str(e)

        }

    return {

        "status": True,

        "message":
        "Leave applied successfully.",

        "data": {

            "leave_id":
            leave.id,

            "leave_type":
            leave.leave_type,

            "from_date":
            leave.from_date,

            "to_date":
            leave.to_date,

            "total_days":
            leave.total_days,

            "status":
            leave.status

        }

    }


# ==========================================
# MY LEAVE LIST
# ==========================================

@router.get("/list")
def my_leave_list(

    current_user=Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )

):

    if current_user["role"] != "employee":

        return {

            "status": False,

            "message":
            "Only employee allowed."

        }

    leaves = db.query(
        LeaveRequest
    ).filter(

        LeaveRequest.user_id
        ==
        current_user["id"]

    ).order_by(

        LeaveRequest.created_at.desc()

    ).all()

    data = []

    for row in leaves:

        data.append({

            "id":
            row.id,

            "leave_type":
            row.leave_type,

            "from_date":
            row.from_date,

            "to_date":
            row.to_date,

            "total_days":
            row.total_days,

            "status":
            row.status,

            "created_at":
            row.created_at.isoformat()
            if row.created_at
            else None

        })

    return {

        "status": True,

        "count":
        len(data),

        "data":
        data

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

    if current_user["role"] != "employee":

        return {

            "status": False,

            "message":
            "Only employee allowed."

        }

    leave = db.query(
        LeaveRequest
    ).filter(

        LeaveRequest.id
        ==
        leave_id,

        LeaveRequest.user_id
        ==
        current_user["id"]

    ).first()

    if not leave:

        return {

            "status": False,

            "message":
            "Leave not found."

        }
        
    admin = None

    if leave.approved_by:

        admin = db.query(
            User
        ).filter(

            User.id
            ==
            leave.approved_by

        ).first()

    return {

        "status": True,

        "data": {

            "id":
            leave.id,

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
            leave.approved_by,

            "approved_by_name":
            admin.name if admin else None,

            "approved_by_code":
            admin.employee_code if admin else None,

            "created_at":
            leave.created_at.isoformat()
            if leave.created_at
            else None

        }

    }


# ==========================================
# CANCEL LEAVE
# ==========================================

@router.put("/cancel/{leave_id}")
def cancel_leave(

    leave_id: int,

    current_user=Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )

):

    if current_user["role"] != "employee":

        return {

            "status": False,

            "message":
            "Only employee allowed."

        }

    leave = db.query(
        LeaveRequest
    ).filter(

        LeaveRequest.id
        ==
        leave_id,

        LeaveRequest.user_id
        ==
        current_user["id"]

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
            "Only pending leave can be cancelled."

        }

    leave.status = "Cancelled"
    leave.admin_remarks = None
    leave.approved_by = None
    

    try:

        db.commit()

        db.refresh(
            leave
        )

    except Exception as e:

        db.rollback()

        return {

            "status": False,

            "message":
            str(e)

        }

    return {

        "status": True,

        "message":
        "Leave cancelled successfully.",

        "data": {

            "leave_id":
            leave.id,

            "status":
            leave.status

        }

    }
