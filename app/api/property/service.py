from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.api.property.model import Property
from app.api.property.schema import PropertyCreate


class PropertyService:

    def __init__(self, session: Session):
            self._db = session    


    def list(self) -> list[Property]:
        return self._db.query(Property).all()

    
    def get_by_id(self, id: int) -> Property:
       
        return self._db.query(Property).filter(Property.id == id).first()
          

    #data is prevalidated by pydantic schema. 
    def create(self, data: PropertyCreate, user_name: str) -> Property:

        ##TO DO: add validation e.g. SQL injection, XSS etc
        db_property = Property(
            address=data.address,
            postcode=data.postcode,
            city=data.city,
            rooms=data.rooms,
            created_by=user_name,
        )
        
        self._db.add(db_property)
        self._db.commit()
        self._db.refresh(db_property)
        
        return db_property

    
    def delete(self, id: int) -> bool:

        property = self._db.query(Property).filter(Property.id == id).first()
        
        if property:       
            self._db.delete(property)
            self._db.commit()

        return property is not None