from sqlalchemy import Column, Integer, String, DateTime, func
from app.db.database import Base
from datetime import datetime


class User(Base):
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String(200), nullable=False, index=True)
    username = Column(String(200), nullable=False, index=True)
    role = Column(String(20), nullable=False, index=True)
    hashed_password = Column(String(200), nullable=False)
 
    
   