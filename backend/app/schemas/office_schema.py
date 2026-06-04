from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ======================================
# CREATE OFFICE
# ======================================

class OfficeCreate(BaseModel):

    office_name: str

    address: Optional[str] = None

    latitude: float

    longitude: float

    radius: int = 5


# ======================================
# UPDATE OFFICE
# ======================================

class OfficeUpdate(BaseModel):

    office_name: Optional[str] = None

    address: Optional[str] = None

    latitude: Optional[float] = None

    longitude: Optional[float] = None

    radius: Optional[int] = None

    is_active: Optional[bool] = None


# ======================================
# OFFICE RESPONSE
# ======================================

class OfficeResponse(BaseModel):

    id: int

    office_name: str

    address: Optional[str]

    latitude: float

    longitude: float

    radius: int

    is_active: bool

    class Config:

        from_attributes = True


# ======================================
# OFFICE LIST RESPONSE
# ======================================

class OfficeListResponse(BaseModel):

    status: bool

    count: int

    data: list[OfficeResponse]


# ======================================
# SINGLE OFFICE RESPONSE
# ======================================

class SingleOfficeResponse(BaseModel):

    status: bool

    data: OfficeResponse