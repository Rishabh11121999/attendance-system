from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class HolidayCreate(BaseModel):

    holiday_name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    holiday_date: date

    description: Optional[str] = Field(
        default=None,
        max_length=500
    )

    is_optional: bool = False


class HolidayUpdate(BaseModel):

    holiday_name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    holiday_date: Optional[date] = None

    description: Optional[str] = Field(
        default=None,
        max_length=500
    )

    is_optional: Optional[bool] = None

    is_active: Optional[bool] = None