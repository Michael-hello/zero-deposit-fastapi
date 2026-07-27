from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.database import get_db
from app.api.property.model import Property
from app.api.property.schema import PropertyCreate, PropertyResponse, PropertyList
from app.auth.jwt import get_user_from_token


router = APIRouter(
    prefix="/api/v1/properties",
    tags=["properties"],
    responses={401: {"description": "Unauthorized access"}},
)


#List all properties in the database.
@router.get("", response_model=List[PropertyList])
async def list_properties(
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None),
):
   
    get_user_from_token(authorization)
    
    properties = db.query(Property).all()
    return properties


# return details of a specific property
@router.get("/{property_id}", response_model=PropertyResponse)
async def get_property(
    property_id: int,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None),
):

    get_user_from_token(authorization)
    
    property_obj = db.query(Property).filter(Property.id == property_id).first()
    
    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Property with ID {property_id} not found",
        )
    
    return property_obj


#Create a new property.
@router.post("", response_model=PropertyResponse, status_code=status.HTTP_201_CREATED)
async def create_property(
    property_data: PropertyCreate,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None),
):
    
    user_id = get_user_from_token(authorization)
    
    db_property = Property(
        address=property_data.address,
        postcode=property_data.postcode,
        city=property_data.city,
        rooms=property_data.rooms,
        created_by=user_id,
    )
    
    # Save to database
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    
    return db_property


#delete a property
@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_property(
    property_id: int,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None),
):
    
    get_user_from_token(authorization)
    
    property_obj = db.query(Property).filter(Property.id == property_id).first()
    
    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Property with ID {property_id} not found",
        )
    
    db.delete(property_obj)
    db.commit()
    
    return None
