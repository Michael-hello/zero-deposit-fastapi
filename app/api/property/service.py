from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.api.property.model import Property
from app.api.property.schema import PropertyCreate
import bleach


class PropertyService:

    def __init__(self, session: Session):
            self._db = session    


    def list(self) -> list[Property]:
        return self._db.query(Property).all()

    
    def get_by_id(self, id: int) -> Property:
       
        return self._db.query(Property).filter(Property.id == id).first()
          

    #data is prevalidated by pydantic schema. 
    def create(self, data: PropertyCreate, user_name: str) -> Property:

        #SQL injecion is mitigated by using SQLAlchemy, which uses parameterized queries.
        ##TO DO: add validation against XSS 
        db_property = Property(
            address=_sanitize_input(data.address),
            postcode=_sanitize_input(data.postcode),
            city=_sanitize_input(data.city),
            rooms=data.rooms,
            created_by=_sanitize_input(user_name),
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


def _sanitize_input(value: str) -> str:
    # Remove all HTML tags, only allow text
    return bleach.clean(value, tags=[], strip=True)