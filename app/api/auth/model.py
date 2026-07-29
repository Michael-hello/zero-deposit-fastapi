from sqlalchemy import CheckConstraint, Column, Integer, String
from app.db.database import Base


class User(Base):
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    
    username = Column(String(200), nullable=False, index=True)
    hashed_password = Column(String(200), nullable=False)
 
    role = Column(String(20), nullable=False, index=True)
    
    __table_args__ = (
        CheckConstraint("role IN ('admin', 'standard')"),
    )


