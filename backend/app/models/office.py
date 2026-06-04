from sqlalchemy import Column, Integer, String, Text, DECIMAL, Boolean, TIMESTAMP
from sqlalchemy.sql import func

from app.database.db import Base


class Office(Base):

    __tablename__ = "offices"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    office_name = Column(
        String(100),
        nullable=False
    )

    address = Column(
        Text,
        nullable=True
    )

    latitude = Column(
        DECIMAL(10, 8),
        nullable=True
    )

    longitude = Column(
        DECIMAL(11, 8),
        nullable=True
    )

    radius = Column(
        Integer,
        default=5
    )

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )