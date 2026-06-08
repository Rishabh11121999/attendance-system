from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class LeaveCreate(BaseModel):

    leave_type: str = Field(
        ...,
        min_length=2,
        max_length=50
    )

    from_date: date

    to_date: date

    reason: Optional[str] = Field(
        default=None,
        max_length=500
    )


class LeaveAction(BaseModel):

    admin_remarks: Optional[str] = Field(
        default=None,
        max_length=500
    )