from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import List, Optional

from app.api.property.service import PropertyService
from app.db.database import SessionLocal
from app.api.property.model import Property
from app.api.property.schema import PropertyCreate, PropertyResponse, PropertyList
from app.auth.jwt import get_user_from_token


router = APIRouter(
    prefix="/api/v1/properties",
    tags=["properties"],
    responses={401: {"description": "Unauthorized access"}},
)


def get_property_service() -> PropertyService:
    return PropertyService(session=SessionLocal())


#List all properties in the database.
@router.get("", response_model=List[PropertyList])
async def list_properties(
    service: PropertyService = Depends(get_property_service),
    authorization: Optional[str] = Header(None),
):
   
    get_user_from_token(authorization)
    
    properties = service.list()
    return properties


# return details of a specific property
@router.get("/{property_id}", response_model=PropertyResponse)
async def get_property(
    property_id: int,
    service: PropertyService = Depends(get_property_service),
    authorization: Optional[str] = Header(None),
):

    get_user_from_token(authorization)
    
    property_obj = service.get_by_id(property_id)
    
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
    service: PropertyService = Depends(get_property_service),
    authorization: Optional[str] = Header(None),
):
    
    user_id = get_user_from_token(authorization)
    
    db_property = service.create(property_data=property_data, user_id=user_id)
    return db_property


#delete a property
@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_property(
    property_id: int,
    service: PropertyService = Depends(get_property_service),
    authorization: Optional[str] = Header(None),
):
    
    get_user_from_token(authorization)
    
    deleted = service.delete(property_id=property_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Property with ID {property_id} not found",
        )
    
    return None
