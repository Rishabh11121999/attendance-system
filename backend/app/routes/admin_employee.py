from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.db import get_db

from app.schemas.employee_schema import (
    EmployeeCreate,
    EmployeeUpdate
)

from app.models.user import User

from app.utils.auth_middleware import (
    get_current_user
)

from app.services.auth_service import (
    hash_password
)


router = APIRouter(

    prefix="/admin/employees",

    tags=["Employee Management"]

)


# ==========================================
# GENERATE EMPLOYEE CODE
# ==========================================

def generate_employee_code(
    db: Session
):

    last_employee = db.query(
        User
    ).order_by(
        User.id.desc()
    ).first()

    if not last_employee:

        return "EMP0001"

    return f"EMP{str(last_employee.id + 1).zfill(4)}"


# ==========================================
# CREATE EMPLOYEE
# ==========================================

@router.post("/create")
def create_employee(

    payload: EmployeeCreate,

    current_user=Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )

):

    # --------------------------------
    # Admin Validation
    # --------------------------------

    if current_user["role"] != "admin":

        return {

            "status": False,

            "message":
            "Only admin can create employee."

        }

    # --------------------------------
    # Duplicate Email Check
    # --------------------------------

    existing = db.query(
        User
    ).filter(

        User.email
        ==
        payload.email

    ).first()

    if existing:

        return {

            "status": False,

            "message":
            "Email already exists."

        }

    # --------------------------------
    # Generate Employee Code
    # --------------------------------

    employee_code = generate_employee_code(
        db
    )

    # --------------------------------
    # Save Employee
    # --------------------------------

    employee = User(

        employee_code=employee_code,

        name=payload.name,

        email=payload.email,

        phone=payload.phone,

        department=payload.department,

        designation=payload.designation,

        joining_date=payload.joining_date,

        password=hash_password(
            payload.password
        ),

        role=payload.role,

        is_active=True

    )

    db.add(
        employee
    )

    db.commit()

    db.refresh(
        employee
    )

    return {

        "status": True,

        "message":
        "Employee created successfully.",

        "data": {

            "id":
            employee.id,

            "employee_code":
            employee.employee_code,

            "name":
            employee.name,

            "email":
            employee.email,

            "phone":
            employee.phone,

            "department":
            employee.department,

            "designation":
            employee.designation,

            "joining_date":
            employee.joining_date,

            "role":
            employee.role,

            "is_active":
            employee.is_active

        }

    }


# ==========================================
# EMPLOYEE LIST
# ==========================================

@router.get("/list")
def employee_list(

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

    employees = db.query(
        User
    ).filter(
        User.role == "employee"
    ).all()

    data = []

    for emp in employees:

        data.append({

            "id":
            emp.id,

            "employee_code":
            emp.employee_code,

            "name":
            emp.name,

            "email":
            emp.email,

            "phone":
            emp.phone,

            "department":
            emp.department,

            "designation":
            emp.designation,

            "joining_date":
            emp.joining_date,

            "role":
            emp.role,

            "is_active":
            emp.is_active

        })

    return {

        "status": True,

        "count":
        len(data),

        "data":
        data

    }
    

# ==========================================
# ACTIVE EMPLOYEES
# ==========================================

@router.get("/active")
def active_employees(

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    if current_user["role"] != "admin":

        return {
            "status": False,
            "message": "Only admin allowed."
        }

    employees = db.query(User).filter(
        User.role == "employee",
        User.is_active == True
    ).all()

    data = []

    for emp in employees:

        data.append({

            "id": emp.id,
            "employee_code": emp.employee_code,
            "name": emp.name,
            "email": emp.email,
            "phone": emp.phone,
            "department": emp.department,
            "designation": emp.designation,
            "joining_date": emp.joining_date

        })

    return {

        "status": True,

        "count": len(data),

        "data": data

    }

# ==========================================
# INACTIVE EMPLOYEES
# ==========================================

@router.get("/inactive")
def inactive_employees(

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    if current_user["role"] != "admin":

        return {
            "status": False,
            "message": "Only admin allowed."
        }

    employees = db.query(User).filter(
        User.role == "employee",
        User.is_active == False
    ).all()

    data = []

    for emp in employees:

        data.append({

            "id": emp.id,
            "employee_code": emp.employee_code,
            "name": emp.name,
            "email": emp.email,
            "phone": emp.phone,
            "department": emp.department,
            "designation": emp.designation,
            "joining_date": emp.joining_date

        })

    return {

        "status": True,

        "count": len(data),

        "data": data

    }


# ==========================================
# EMPLOYEE DETAILS
# ==========================================

@router.get("/details/{user_id}")
def employee_details(

    user_id: int,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    if current_user["role"] != "admin":

        return {
            "status": False,
            "message": "Only admin allowed."
        }

    employee = db.query(User).filter(
        User.id == user_id,
        User.role == "employee"
    ).first()

    if not employee:

        return {
            "status": False,
            "message": "Employee not found."
        }

    return {

        "status": True,

        "data": {

            "id": employee.id,
            "employee_code": employee.employee_code,
            "name": employee.name,
            "email": employee.email,
            "phone": employee.phone,
            "department": employee.department,
            "designation": employee.designation,
            "joining_date": employee.joining_date,
            "role": employee.role,
            "is_active": employee.is_active

        }

    } 
    
    
# ==========================================
# UPDATE EMPLOYEE
# ==========================================

@router.put("/update/{user_id}")
def update_employee(

    user_id: int,

    payload: EmployeeUpdate,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    if current_user["role"] != "admin":

        return {
            "status": False,
            "message": "Only admin allowed."
        }

    employee = db.query(User).filter(
        User.id == user_id,
        User.role == "employee"
    ).first()

    if not employee:

        return {
            "status": False,
            "message": "Employee not found."
        }

    if payload.email:

        existing = db.query(User).filter(
            User.email == payload.email,
            User.id != user_id
        ).first()

        if existing:

            return {
                "status": False,
                "message": "Email already exists."
            }

    update_data = payload.dict(
        exclude_unset=True
    )

    for key, value in update_data.items():

        setattr(
            employee,
            key,
            value
        )

    db.commit()

    db.refresh(employee)

    return {

        "status": True,

        "message":
        "Employee updated successfully."

    }
    
# ==========================================
# DELETE EMPLOYEE
# ==========================================

@router.delete("/delete/{user_id}")
def delete_employee(

    user_id: int,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    if current_user["role"] != "admin":

        return {
            "status": False,
            "message": "Only admin allowed."
        }

    employee = db.query(User).filter(
        User.id == user_id,
        User.role == "employee"
    ).first()

    if not employee:

        return {
            "status": False,
            "message": "Employee not found."
        }

    employee.is_active = False

    db.commit()

    return {

        "status": True,

        "message":
        "Employee deleted successfully."

    }
    
# ==========================================
# RESTORE EMPLOYEE
# ==========================================

@router.put("/restore/{user_id}")
def restore_employee(

    user_id: int,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    if current_user["role"] != "admin":

        return {
            "status": False,
            "message": "Only admin allowed."
        }

    employee = db.query(User).filter(
        User.id == user_id,
        User.role == "employee"
    ).first()

    if not employee:

        return {
            "status": False,
            "message": "Employee not found."
        }

    employee.is_active = True

    db.commit()

    return {

        "status": True,

        "message":
        "Employee restored successfully."

    }

