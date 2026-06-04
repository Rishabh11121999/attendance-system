from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db

from app.utils.auth_middleware import (
    get_current_user
)

from app.schemas.assignment_schema import (
    AssignmentCreate,
    AssignmentUpdate
)

from app.models.user import User
from app.models.office import Office
from app.models.employee_office import EmployeeOffice

router = APIRouter(
    prefix="/admin/assignments",
    tags=["Employee Office Assignment"]
)


# =====================================
# CREATE ASSIGNMENT
# =====================================

@router.post("/create")
def create_assignment(

    payload: AssignmentCreate,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    if current_user["role"] != "admin":

        return {
            "status": False,
            "message": "Only admin can assign office."
        }

    user = db.query(User).filter(
        User.id == payload.user_id
    ).first()

    if not user:

        return {
            "status": False,
            "message": "Employee not found."
        }

    office = db.query(Office).filter(
        Office.id == payload.office_id,
        Office.is_active == True
    ).first()

    if not office:

        return {
            "status": False,
            "message": "Office not found."
        }

    already = db.query(
        EmployeeOffice
    ).filter(
        EmployeeOffice.user_id == payload.user_id,
        EmployeeOffice.is_active == True
    ).first()

    if already:

        return {
            "status": False,
            "message": "Employee already assigned to an office."
        }

    assignment = EmployeeOffice(

        user_id=payload.user_id,

        office_id=payload.office_id,

        start_date=payload.start_date,

        end_date=payload.end_date,

        remarks=payload.remarks,

        assigned_by=current_user["id"],

        is_active=True

    )

    db.add(assignment)

    db.commit()

    db.refresh(assignment)

    return {

        "status": True,

        "message": "Office assigned successfully.",

        "data": {

            "assignment_id": assignment.id,

            "employee_id": assignment.user_id,

            "office_id": assignment.office_id,

            "start_date": assignment.start_date,

            "end_date": assignment.end_date,

            "assigned_by": assignment.assigned_by,

            "remarks": assignment.remarks

        }

    }


# =====================================
# ASSIGNMENT LIST
# =====================================

@router.get("/list")
def assignment_list(

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    if current_user["role"] != "admin":

        return {
            "status": False,
            "message": "Only admin allowed."
        }

    assignments = db.query(
        EmployeeOffice
    ).all()

    data = []

    for row in assignments:

        employee = db.query(User).filter(
            User.id == row.user_id
        ).first()

        office = db.query(Office).filter(
            Office.id == row.office_id
        ).first()

        data.append({

            "id": row.id,

            "employee_id": row.user_id,

            "employee_name":
            employee.name if employee else None,

            "office_id": row.office_id,

            "office_name":
            office.office_name if office else None,

            "start_date": row.start_date,

            "end_date": row.end_date,

            "is_active": row.is_active,

            "remarks": row.remarks

        })

    return {

        "status": True,

        "count": len(data),

        "data": data

    }


# =====================================
# ASSIGNMENT DETAILS
# =====================================

@router.get("/{assignment_id}")
def assignment_details(

    assignment_id: int,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    row = db.query(
        EmployeeOffice
    ).filter(
        EmployeeOffice.id == assignment_id
    ).first()

    if not row:

        return {
            "status": False,
            "message": "Assignment not found."
        }

    employee = db.query(User).filter(
        User.id == row.user_id
    ).first()

    office = db.query(Office).filter(
        Office.id == row.office_id
    ).first()

    return {

        "status": True,

        "data": {

            "id": row.id,

            "employee_id": row.user_id,

            "employee_name":
            employee.name if employee else None,

            "office_id": row.office_id,

            "office_name":
            office.office_name if office else None,

            "start_date": row.start_date,

            "end_date": row.end_date,

            "is_active": row.is_active,

            "remarks": row.remarks

        }

    }


# =====================================
# UPDATE ASSIGNMENT
# =====================================

@router.put("/update/{assignment_id}")
def update_assignment(

    assignment_id: int,

    payload: AssignmentUpdate,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    assignment = db.query(
        EmployeeOffice
    ).filter(
        EmployeeOffice.id == assignment_id
    ).first()

    if not assignment:

        return {
            "status": False,
            "message": "Assignment not found."
        }

    update_data = payload.dict(
        exclude_unset=True
    )

    for key, value in update_data.items():

        setattr(
            assignment,
            key,
            value
        )

    db.commit()

    db.refresh(assignment)

    return {

        "status": True,

        "message":
        "Assignment updated successfully."

    }


# =====================================
# DELETE ASSIGNMENT
# =====================================

@router.delete("/delete/{assignment_id}")
def delete_assignment(

    assignment_id: int,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    assignment = db.query(
        EmployeeOffice
    ).filter(
        EmployeeOffice.id == assignment_id
    ).first()

    if not assignment:

        return {
            "status": False,
            "message": "Assignment not found."
        }

    assignment.is_active = False

    db.commit()

    return {

        "status": True,

        "message":
        "Assignment deleted successfully."

    }


# =====================================
# RESTORE ASSIGNMENT
# =====================================

@router.put("/restore/{assignment_id}")
def restore_assignment(

    assignment_id: int,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    assignment = db.query(
        EmployeeOffice
    ).filter(
        EmployeeOffice.id == assignment_id
    ).first()

    if not assignment:

        return {
            "status": False,
            "message": "Assignment not found."
        }

    assignment.is_active = True

    db.commit()

    return {

        "status": True,

        "message":
        "Assignment restored successfully."

    }