from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import Text
from sqlalchemy import TIMESTAMP
from sqlalchemy.sql import func

from app.database.db import Base


class LeaveRequest(Base):

    __tablename__ = "leave_requests"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        nullable=False
    )

    leave_type = Column(
        String(50),
        nullable=False
    )

    from_date = Column(
        Date,
        nullable=False
    )

    to_date = Column(
        Date,
        nullable=False
    )

    total_days = Column(
        Integer,
        nullable=False
    )

    reason = Column(
        Text,
        nullable=True
    )

    status = Column(
        String(20),
        default="Pending"
    )

    approved_by = Column(
        Integer,
        nullable=True
    )

    admin_remarks = Column(
        Text,
        nullable=True
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