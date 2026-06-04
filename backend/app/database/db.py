from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


from dotenv import load_dotenv
from urllib.parse import quote_plus

import os

load_dotenv()

DB_HOST = os.getenv(
    "DB_HOST"
)

DB_NAME = os.getenv(
    "DB_NAME"
)

DB_USER = os.getenv(
    "DB_USER"
)

DB_PASSWORD = quote_plus(
    os.getenv(
        "DB_PASSWORD"
    )
)

DATABASE_URL = (

    f"mysql+pymysql://"

    f"{DB_USER}:"

    f"{DB_PASSWORD}"

    f"@{DB_HOST}/"

    f"{DB_NAME}"

)

engine = create_engine(

    DATABASE_URL,

    pool_pre_ping=True

)

SessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine

)

# --------------------------
# SQLAlchemy Base
# --------------------------

Base = declarative_base()


# --------------------------
# Database Dependency
# --------------------------

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()