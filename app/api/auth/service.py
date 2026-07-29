import bleach
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from .schema import UserCreate, UserLoginRequest
from .model import User
from app.auth.utils import hash_password, verify_password

class UserService:

    def __init__(self, session: Session):
            self._db = session

    def create(self, user: UserCreate) -> User:

        existing_user = self._db.query(User).filter(User.username == user.username).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Invalid username"
            )

        ##TO DO: add password validation logic
        hashed_password = hash_password(user.password)
        
        db_user = User(
            username=_sanitize_input(user.username),
            hashed_password=_sanitize_input(hashed_password),
            role="standard",
        )

        self._db.add(db_user)
        self._db.commit()
        self._db.refresh(db_user)

        return db_user


    def get_user(self, username: str) -> User:
        return self._db.query(User).filter(User.username == username).first()


    def login(self, user: UserLoginRequest) -> User:
        db_user = self.authenticate_user(user.username, user.password)
           
        return db_user


    def authenticate_user(self, username: str, password: str) -> User:
        user = self.get_user(username)

        if not user or not verify_password(password, user.hashed_password):
             raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user



def _sanitize_input(value: str) -> str:
    # Remove all HTML tags, only allow text
    return bleach.clean(value, tags=[], strip=True)