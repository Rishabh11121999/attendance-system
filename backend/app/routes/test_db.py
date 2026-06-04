from fastapi import APIRouter, Depends

from app.utils.auth_middleware import (
    get_current_user
)

router = APIRouter()


@router.get("/profile")
def profile(

    current_user=Depends(
        get_current_user
    )

):

    return {

        "status": True,

        "user": current_user

    }