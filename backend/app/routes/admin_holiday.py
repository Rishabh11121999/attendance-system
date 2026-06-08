from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.db import get_db

from app.utils.auth_middleware import (
    get_current_user
)

from app.models.holiday import (
    Holiday
)

from app.schemas.holiday_schema import (
    HolidayCreate,
    HolidayUpdate
)



router = APIRouter(

    prefix="/admin/holidays",

    tags=["Holiday Management"]

)


# ==========================================
# CREATE HOLIDAY
# ==========================================

@router.post("/create")
def create_holiday(

    payload: HolidayCreate,

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

    already = db.query(
        Holiday
    ).filter(

        Holiday.holiday_date
        ==
        payload.holiday_date,

        Holiday.is_active
        ==
        True

    ).first()

    if already:

        return {

            "status": False,

            "message":
            "Holiday already exists."

        }

    holiday = Holiday(

        holiday_name=payload.holiday_name,

        holiday_date=payload.holiday_date,

        description=payload.description,

        is_optional=payload.is_optional,

        is_active=True

    )

    try:

        db.add(
            holiday
        )

        db.commit()

        db.refresh(
            holiday
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
        "Holiday created successfully.",

        "data": {

            "id":
            holiday.id,

            "holiday_name":
            holiday.holiday_name,

            "holiday_date":
            holiday.holiday_date

        }

    }


# ==========================================
# HOLIDAY LIST
# ==========================================

@router.get("/list")
def holiday_list(

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

    holidays = db.query(
        Holiday
    ).order_by(

        Holiday.holiday_date.asc()

    ).all()

    data = []

    for row in holidays:

        data.append({

            "id":
            row.id,

            "holiday_name":
            row.holiday_name,

            "holiday_date":
            row.holiday_date,

            "description":
            row.description,

            "is_optional":
            row.is_optional,

            "is_active":
            row.is_active

        })

    return {

        "status": True,

        "count":
        len(data),

        "data":
        data

    }




# ==========================================
# UPDATE HOLIDAY
# ==========================================

@router.put("/update/{holiday_id}")
def update_holiday(

    holiday_id: int,

    payload: HolidayUpdate,

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

    holiday = db.query(
        Holiday
    ).filter(

        Holiday.id
        ==
        holiday_id

    ).first()

    if not holiday:

        return {

            "status": False,

            "message":
            "Holiday not found."

        }

    update_data = payload.model_dump(
        exclude_unset=True
    )

    # Prevent duplicate holiday date
    if "holiday_date" in update_data:

        duplicate = db.query(
            Holiday
        ).filter(

            Holiday.id != holiday_id,

            Holiday.holiday_date
            ==
            update_data["holiday_date"],

            Holiday.is_active
            ==
            True

        ).first()

        if duplicate:

            return {

                "status": False,

                "message":
                "Another holiday already exists on this date."

            }

    for key, value in update_data.items():

        setattr(

            holiday,

            key,

            value

        )

    try:

        db.commit()

        db.refresh(
            holiday
        )

        return {

            "status": True,

            "message":
            "Holiday updated successfully."

        }

    except Exception as e:

        db.rollback()

        return {

            "status": False,

            "message":
            str(e)

        }

# ==========================================
# DELETE HOLIDAY
# ==========================================

@router.delete("/delete/{holiday_id}")
def delete_holiday(

    holiday_id: int,

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

    holiday = db.query(
        Holiday
    ).filter(

        Holiday.id
        ==
        holiday_id

    ).first()

    if not holiday:

        return {

            "status": False,

            "message":
            "Holiday not found."

        }
    
    if not holiday.is_active:

        return {

            "status": False,

            "message":
            "Holiday already inactive."

        }

    holiday.is_active = False

    try:

        db.commit()

        db.refresh(
            holiday
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
        "Holiday deleted successfully."

    }


# ==========================================
# RESTORE HOLIDAY
# ==========================================

@router.put("/restore/{holiday_id}")
def restore_holiday(

    holiday_id: int,

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

    holiday = db.query(
        Holiday
    ).filter(

        Holiday.id
        ==
        holiday_id

    ).first()

    if not holiday:

        return {

            "status": False,

            "message":
            "Holiday not found."

        }
    if holiday.is_active:

        return {

            "status": False,

            "message":
            "Holiday already active."

        }

    holiday.is_active = True

    try:

        db.commit()

        db.refresh(
            holiday
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
        "Holiday restored successfully."

    }


# ==========================================
# ACTIVE HOLIDAYS
# ==========================================

@router.get("/active")
def active_holidays(

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
        Holiday
    ).filter(

        Holiday.is_active
        ==
        True

    ).order_by(

        Holiday.holiday_date.asc()

    ).all()

    data = []

    for row in records:

        data.append({

            "id":
            row.id,

            "holiday_name":
            row.holiday_name,

            "holiday_date":
            row.holiday_date,

            "description":
            row.description,

            "is_optional":
            row.is_optional,

            "is_active":
            row.is_active

        })

    return {

        "status": True,

        "count":
        len(data),

        "data":
        data

    }


# ==========================================
# INACTIVE HOLIDAYS
# ==========================================

@router.get("/inactive")
def inactive_holidays(

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
        Holiday
    ).filter(

        Holiday.is_active
        ==
        False

    ).order_by(

        Holiday.holiday_date.asc()

    ).all()

    data = []

    for row in records:

        data.append({

            "id":
            row.id,

            "holiday_name":
            row.holiday_name,

            "holiday_date":
            row.holiday_date,

            "description":
            row.description,

            "is_optional":
            row.is_optional,

            "is_active":
            row.is_active

        })

    return {

        "status": True,

        "count":
        len(data),

        "data":
        data

    }
    
    
# ==========================================
# HOLIDAY DETAILS
# ==========================================

@router.get("/{holiday_id}")
def holiday_details(

    holiday_id: int,

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

    holiday = db.query(
        Holiday
    ).filter(

        Holiday.id
        ==
        holiday_id

    ).first()

    if not holiday:

        return {

            "status": False,

            "message":
            "Holiday not found."

        }

    return {

        "status": True,

        "data": {

            "id":
            holiday.id,

            "holiday_name":
            holiday.holiday_name,

            "holiday_date":
            holiday.holiday_date,

            "description":
            holiday.description,

            "is_optional":
            holiday.is_optional,

            "is_active":
            holiday.is_active

        }

    }
