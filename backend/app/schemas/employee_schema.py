from pydantic import BaseModel
from typing import Optional
from datetime import date


class EmployeeCreate(BaseModel):

    name: str

    email: str

    phone: Optional[str] = None

    department: Optional[str] = None

    designation: Optional[str] = None

    joining_date: Optional[date] = None

    password: str

    role: str = "employee"


class EmployeeUpdate(BaseModel):

    name: Optional[str] = None

    email: Optional[str] = None

    phone: Optional[str] = None

    department: Optional[str] = None

    designation: Optional[str] = None

    joining_date: Optional[date] = None

    role: Optional[str] = None

    is_active: Optional[bool] = None