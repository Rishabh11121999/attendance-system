from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.db import get_db

from app.schemas.office_schema import (
    OfficeCreate,
    OfficeUpdate
)

from app.models.office import Office

from app.utils.auth_middleware import (
    get_current_user
)

router = APIRouter(
    prefix="/admin/offices",
    tags=["Office Management"]
)


# ======================================
# CREATE OFFICE
# ======================================

@router.post("/create")
def create_office(
    office: OfficeCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if current_user["role"] != "admin":

        return {
            "status": False,
            "message": "Only admin can create office."
        }

    existing = db.query(
        Office
    ).filter(
        Office.office_name == office.office_name
    ).first()

    if existing:

        return {
            "status": False,
            "message": "Office already exists."
        }

    new_office = Office(

        office_name=office.office_name,

        address=office.address,

        latitude=office.latitude,

        longitude=office.longitude,

        radius=office.radius,

        is_active=True

    )

    db.add(new_office)

    db.commit()

    db.refresh(new_office)

    return {

        "status": True,

        "message":
        "Office created successfully.",

        "office": {

            "id":
            new_office.id,

            "office_name":
            new_office.office_name,

            "address":
            new_office.address,

            "latitude":
            float(new_office.latitude),

            "longitude":
            float(new_office.longitude),

            "radius":
            new_office.radius

        }

    }


# ======================================
# OFFICE LIST
# ======================================

@router.get("/list")
def office_list(

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    if current_user["role"] != "admin":

        return {

            "status": False,

            "message":
            "Only admin can view offices."

        }

    offices = db.query(
        Office
    ).filter(
        Office.is_active == True
    ).all()

    data = []

    for office in offices:

        data.append({

            "id":
            office.id,

            "office_name":
            office.office_name,

            "address":
            office.address,

            "latitude":
            float(office.latitude),

            "longitude":
            float(office.longitude),

            "radius":
            office.radius,

            "is_active":
            office.is_active

        })

    return {

        "status": True,

        "count":
        len(data),

        "data":
        data

    }


# ======================================
# OFFICE DETAILS
# ======================================

@router.get("/{office_id}")
def office_details(

    office_id: int,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

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

    return {

        "status": True,

        "data": {

            "id":
            office.id,

            "office_name":
            office.office_name,

            "address":
            office.address,

            "latitude":
            float(office.latitude),

            "longitude":
            float(office.longitude),

            "radius":
            office.radius,

            "is_active":
            office.is_active

        }

    }


# ======================================
# UPDATE OFFICE
# ======================================

@router.put("/update/{office_id}")
def update_office(

    office_id: int,

    payload: OfficeUpdate,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

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

    update_data = payload.dict(
        exclude_unset=True
    )

    for key, value in update_data.items():

        setattr(
            office,
            key,
            value
        )

    db.commit()

    db.refresh(
        office
    )

    return {

        "status": True,

        "message":
        "Office updated successfully."

    }


# ======================================
# DELETE OFFICE
# ======================================

@router.delete("/delete/{office_id}")
def delete_office(

    office_id: int,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

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

    office.is_active = False

    db.commit()

    return {

        "status": True,

        "message":
        "Office deleted successfully."

    }
    
    # ======================================
# RESTORE OFFICE
# ======================================

@router.put("/restore/{office_id}")
def restore_office(

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

    office.is_active = True

    db.commit()

    db.refresh(office)

    return {

        "status": True,

        "message":
        "Office restored successfully."

    }