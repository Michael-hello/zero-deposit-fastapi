from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    username: str = Field(..., min_length=1, max_length=50, description="Username")


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=50, description="Password")


class User(UserBase):

    model_config = ConfigDict(from_attributes=True)
    id: int

