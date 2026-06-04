from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.user_schema import (
    RegisterSchema,
    LoginSchema
)

from app.database.db import get_db
from app.models.user import User
from app.services.auth_service import (
    hash_password
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
        "message":
        "User Registered Successfully"
    }


@router.post("/login")
def login(
    user: LoginSchema
):

    return {
        "message":
        "Login API Working"
    }