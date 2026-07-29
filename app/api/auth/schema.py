from pydantic import BaseModel, Field
from .model import User


class UserCreate(BaseModel):

    password: str = Field(..., min_length=8, max_length=50, description="Password")
    username: str = Field(..., min_length=1, max_length=50, description="Username")


class UserLoginRequest(UserCreate):
    pass


class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreateResponse(BaseModel):

    id: int
    username: str
    role: str

    def fromUser(self, user: User):
        self.id = user.id
        self.username = user.username
        self.role = user.role

