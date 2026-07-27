from sqlalchemy import Column, Integer, String, DateTime, func
from app.db.database import Base
from datetime import datetime


class Property(Base):
    
    __tablename__ = "properties"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    address = Column(String(255), nullable=False, index=True)
    postcode = Column(String(20), nullable=False, index=True)
    city = Column(String(100), nullable=False, index=True)
    rooms = Column(Integer, nullable=False)
    
    created_by = Column(String(255), nullable=False)  
    
   