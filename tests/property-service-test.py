import pytest
from app.api.property.service import PropertyService
from app.api.property.schema import PropertyCreate
from tests.helpers import init_test_db

#to run this file individually: pytest tests/property-service-test.py -v

def test_create():
    """Test PropertyService.create """
    
    mock_session = init_test_db()  
    service = PropertyService(session=mock_session)
    
    property_data = PropertyCreate(
        address="11 Main St",
        postcode="LL33 0DD",
        city="Conwy",
        rooms=3
    )
    user_name = "Bob Geldof"

    _property = service.create(property_data, user_name)
    created_property = service.get_by_id(_property.id)  
    
    assert created_property.address == "11 Main St"
    assert created_property.postcode == "LL33 0DD"
    assert created_property.city == "Conwy"
    assert created_property.rooms == 3
    assert created_property.created_by == user_name



def test_list():
    """Test PropertyService.list """
    
    mock_session = init_test_db()  
    service = PropertyService(session=mock_session)
    
    property_data1 = PropertyCreate(
        address="11 Main St",
        postcode="LL33 0DD",
        city="Conwy",
        rooms=3
    )
    property_data2 = PropertyCreate(
        address="22 High St",
        postcode="LL33 0EE",
        city="Conwy",
        rooms=4
    )
    user_name = "Bob Geldof Junior"

    service.create(property_data1, user_name)
    service.create(property_data2, user_name)

    properties = service.list()
    
    assert len(properties) == 2
    assert properties[0].address == "11 Main St"
    assert properties[1].address == "22 High St"


def test_get_by_id():
    """Test PropertyService.get_by_id """
    
    mock_session = init_test_db()  
    service = PropertyService(session=mock_session)
    
    property_data = PropertyCreate(
        address="11 Main St",
        postcode="LL33 0DD",
        city="Conwy",
        rooms=3
    )
    user_name = "Bob Geldof"

    _property = service.create(property_data, user_name)
    retrieved_property = service.get_by_id(_property.id)  
    
    assert retrieved_property.address == "11 Main St"
    assert retrieved_property.postcode == "LL33 0DD"
    assert retrieved_property.city == "Conwy"
    assert retrieved_property.rooms == 3
    assert retrieved_property.created_by == user_name