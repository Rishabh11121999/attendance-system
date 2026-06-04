from pydantic import BaseModel
from typing import Optional
from datetime import date



class AssignmentCreate(BaseModel):

    user_id: int

    office_id: int

    start_date: date

    end_date: Optional[date] = None

    remarks: Optional[str] = None


class AssignmentUpdate(BaseModel):

    office_id: Optional[int] = None

    start_date: Optional[date] = None

    end_date: Optional[date] = None

    remarks: Optional[str] = None

    is_active: Optional[bool] = None