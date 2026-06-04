from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.user_schema import (
    RegisterSchema,
    LoginSchema
)

from app.database.db import get_db

from app.models.user import User

from app.services.auth_service import (
    hash_password,
    verify_password
)

from app.utils.jwt_handler import (
    create_access_token
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    user: RegisterSchema,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:

        return {

            "status": False,

            "message":
            "Email already exists"

        }

    new_user = User(

        name=user.name,

        email=user.email,

        password=hash_password(
            user.password
        ),

        role=user.role

    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {

        "status": True,

        "message":
        "User Registered Successfully"

    }


@router.post("/login")
def login(
    user: LoginSchema,
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:

        return {

            "status": False,

            "message":
            "Invalid Email"

        }

    if not verify_password(
        user.password,
        db_user.password
    ):

        return {

            "status": False,

            "message":
            "Invalid Password"

        }

    access_token = create_access_token(

        {

            "id": db_user.id,

            "email": db_user.email,

            "role": db_user.role

        }

    )

    return {

        "status": True,

        "message":
        "Login Successful",

        "access_token":
        access_token,

        "token_type":
        "Bearer",

        "user": {

            "id":
            db_user.id,

            "name":
            db_user.name,

            "email":
            db_user.email,

            "role":
            db_user.role

        }

    }