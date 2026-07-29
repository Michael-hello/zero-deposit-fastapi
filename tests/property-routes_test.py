
from fastapi.testclient import TestClient
from app.api.property.routes import get_property_service, get_user_service
from app.api.property.service import PropertyService
from app.api.auth.service import UserService

from app.auth.jwt import create_access_token
from app.main import app
from app.db.database import Base
from tests.helpers import init_test_db

testSession = init_test_db(inMemory=False)
client = TestClient(app)

# override dependencies in the main app
def override_get_property_service():    
    yield PropertyService(session=testSession)

def override_get_user_service():
    yield UserService(session=testSession)


app.dependency_overrides[get_property_service] = override_get_property_service
app.dependency_overrides[get_user_service] = override_get_user_service

username = "testuser"

# Create a JWT token for authorization
token = create_access_token(username=username)
headers = {"Authorization": f"Bearer {token}"}



def test_create_property():
    """Test creating a new property route """
    cleanup_database()
    
    property_data = {
        "address": "12 Main St",
        "postcode": "SW1A 1AA",
        "city": "London",
        "rooms": 3,
    }
    
    response = client.post("/api/v1/properties", json=property_data, headers=headers)
    
    assert response.status_code == 201
    data = response.json()
    assert data["address"] == "12 Main St"
    assert data["postcode"] == "SW1A 1AA"
    assert data["city"] == "London"
    assert data["rooms"] == 3
    assert "id" in data
    assert "created_by" in data




#TO DO: add better data handling for test cases
def cleanup_database():
    """Cleanup the database after tests"""
    # Delete all rows from all tables
    for table in reversed(Base.metadata.sorted_tables):
        testSession.execute(table.delete())
    testSession.commit()