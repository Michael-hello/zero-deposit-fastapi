from fastapi import status
from fastapi import APIRouter, Depends

from app.db.database import SessionLocal
from app.auth.jwt import create_access_token

from .service import UserService
from .schema import UserCreate, UserCreateResponse, UserLoginRequest, UserLoginResponse


router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"],
    responses={401: {"description": "Unauthorized access"}},
)

def get_user_service() -> UserService:
    return UserService(session=SessionLocal())


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserCreateResponse)
async def create_user(
    create_user_request: UserCreate,
    service: UserService = Depends(get_user_service),
):
    user = service.create(create_user_request)

    response = UserCreateResponse(username=user.username, id=user.id, role=user.role)
    return response


@router.post("/login", status_code=status.HTTP_201_CREATED, response_model=UserLoginResponse)
async def login_user(
    login_request: UserLoginRequest,
    service: UserService = Depends(get_user_service),
):

    user = service.login(login_request)
    
    token = create_access_token(data={"sub": user.username})
    return UserLoginResponse(access_token=token)
    