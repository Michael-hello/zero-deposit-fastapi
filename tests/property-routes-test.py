import jwt
from fastapi.testclient import TestClient
from app.api.property.routes import get_property_service
from app.api.property.service import PropertyService

from app.main import app
from app.db.database import Base
from tests.helpers import init_test_db

testSession = init_test_db()
client = TestClient(app)

# override dependency in the main app
def override_get_property_service():
    
    yield PropertyService(session=testSession)


app.dependency_overrides[get_property_service] = override_get_property_service


    
def test_create_property():
    """Test creating a new property route """
    cleanup_database()
    
    property_data = {
        "address": "12 Main St",
        "postcode": "SW1A 1AA",
        "city": "London",
        "rooms": 3,
    }
    
    response = client.post("/api/v1/properties", json=property_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["address"] == "12 Main St"
    assert data["postcode"] == "SW1A 1AA"
    assert data["city"] == "London"
    assert data["rooms"] == 3
    assert "id" in data
    assert "created_by" in data


def test_list_properties():
    """Test listing all properties"""
    cleanup_database()
    
    # Create two properties with different users
    for i in range(2):
        property_data = {
            "address": f"{i} Main St",
            "postcode": "SW1A 1AA",
            "city": "London",
            "rooms": i + 1,
        }
        client.post("/api/v1/properties", json=property_data)
    
    response = client.get("/api/v1/properties")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["address"] == "0 Main St"
    assert data[1]["address"] == "1 Main St"



#TO DO: add better data handling for test cases
def cleanup_database():
    """Cleanup the database after tests"""
    # Delete all rows from all tables
    for table in reversed(Base.metadata.sorted_tables):
        testSession.execute(table.delete())
    testSession.commit()