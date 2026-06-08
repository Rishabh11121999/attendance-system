from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from datetime import date

from app.database.db import get_db

from app.utils.auth_middleware import (
    get_current_user
)

from app.models.holiday import (
    Holiday
)

router = APIRouter(

    prefix="/employee/holidays",

    tags=["Employee Holidays"]

)


# ==========================================
# UPCOMING HOLIDAYS
# ==========================================

@router.get("/")
def employee_holidays(

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

    try:

        holidays = db.query(
            Holiday
        ).filter(

            Holiday.is_active
            ==
            True,

            Holiday.holiday_date
            >=
            date.today()

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
                row.holiday_date.isoformat()
                if row.holiday_date
                else None,

                "description":
                row.description,

                "is_optional":
                row.is_optional

            })

        return {

            "status": True,

            "count":
            len(data),

            "data":
            data

        }

    except Exception as e:

        return {

            "status": False,

            "message":
            str(e)

        }
        
# ==========================================
# OPTIONAL HOLIDAYS
# ==========================================

@router.get("/optional/list")
def optional_holidays(

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

    try:

        holidays = db.query(
            Holiday
        ).filter(

            Holiday.is_active
            ==
            True,

            Holiday.is_optional
            ==
            True,

            Holiday.holiday_date
            >=
            date.today()

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
                row.holiday_date.isoformat()
                if row.holiday_date
                else None,

                "description":
                row.description,

                "is_optional":
                row.is_optional

            })

        return {

            "status": True,

            "count":
            len(data),

            "data":
            data

        }

    except Exception as e:

        return {

            "status": False,

            "message":
            str(e)

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

    if current_user["role"] != "employee":

        return {

            "status": False,

            "message":
            "Only employee allowed."

        }

    holiday = db.query(
        Holiday
    ).filter(

        Holiday.id
        ==
        holiday_id,

        Holiday.is_active
        ==
        True

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
            holiday.holiday_date.isoformat()
            if holiday.holiday_date
            else None,

            "description":
            holiday.description,

            "is_optional":
            holiday.is_optional

        }

    }


