from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.api.property.model import Property
from app.api.property.schema import PropertyCreate


class PropertyService:

    def __init__(self, session: Session):
            self._db = session    


    def list(self) -> list[Property]:
        return self._db.query(Property).all()

    
    def get_by_id(self, property_id: int) -> Property:
       
        return self._db.query(Property).filter(Property.id == property_id).first()
          
    
    def create(self, property_data: PropertyCreate, user_id: str) -> Property:

        ##TO DO: add validation
        db_property = Property(
            address=property_data.address,
            postcode=property_data.postcode,
            city=property_data.city,
            rooms=property_data.rooms,
            created_by=user_id,
        )
        
        self._db.add(db_property)
        self._db.commit()
        self._db.refresh(db_property)
        
        return db_property

    
    def delete(self, property_id: int) -> bool:

        property_obj = self._db.query(Property).filter(Property.id == property_id).first()
        
        if property_obj:       
            self._db.delete(property_obj)
            self._db.commit()

        return property_obj is not None