from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Date
from sqlalchemy import Text
from sqlalchemy import TIMESTAMP
from sqlalchemy.sql import func

from app.database.db import Base


class Holiday(Base):

    __tablename__ = "holidays"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    holiday_name = Column(
        String(150),
        nullable=False
    )

    holiday_date = Column(
        Date,
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    is_optional = Column(
        Boolean,
        default=False
    )

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )

    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now()
    )