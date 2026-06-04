from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


class CheckInRequest(BaseModel):

    latitude: float
    longitude: float


class CheckOutRequest(BaseModel):

    latitude: float
    longitude: float


class AttendanceResponse(BaseModel):

    status: bool
    message: str
    office_name: Optional[str] = None
    distance: Optional[float] = None
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None


class AttendanceHistoryItem(BaseModel):

    attendance_date: date
    check_in: Optional[datetime]
    check_out: Optional[datetime]
    work_hours: Optional[float]
    status: str


class AttendanceHistoryResponse(BaseModel):

    status: bool
    data: list[AttendanceHistoryItem]