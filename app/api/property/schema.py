from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

# Data validation handled by pydantic and 
# automatically handled by fastapi if fails validation, returns a 422  
class PropertyCreate(BaseModel):
  
    address: str = Field(..., min_length=1, max_length=500, description="Property address")
    postcode: str = Field(..., min_length=1, max_length=20, description="Postal code")
    city: str = Field(..., min_length=1, max_length=100, description="City name")
    rooms: int = Field(..., gt=0, description="Number of rooms")


class PropertyResponse(BaseModel):

    #tells Pydantic to read data from object attributes instead of requiring a dictionary.
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="Property unique ID")
    address: str = Field(..., description="Property address")
    postcode: str = Field(..., description="Postal code")
    city: str = Field(..., description="City name")
    rooms: int = Field(..., description="Number of rooms")
    created_by: str = Field(..., description="User who created the property")




class PropertyList(BaseModel):

    model_config = ConfigDict(from_attributes=True)
    
    id: int
    address: str
    postcode: str
    city: str
    rooms: int
    created_by: str
    
