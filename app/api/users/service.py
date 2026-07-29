from sqlalchemy.orm import Session

class UserService:

    def __init__(self, session: Session):
            self._db = session
