from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .schema import User
from .model import User as UserModel

from app.auth.jwt import get_user_from_token as get_current_user


router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"],
    responses={401: {"description": "Unauthorized access"}},
)

@router.get("/test_user", response_model=User)
def read_users_me(current_user: UserModel = Depends(get_current_user)):
    return current_user