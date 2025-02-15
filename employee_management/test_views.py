import pytest
from rest_framework.test import APIClient
from employee_management.models.models import User,SessionLocal

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def db_session():
    session = SessionLocal()
    yield session
    session.rollback()  # Rollback after test execution
    session.close()

def test_create_user(client, db_session):
    url = "/users/"  # Change this based on your actual URL
    payload = {"name": "Gautam", "email": "gautam@example.com", "password": "securepass"}
    

    db_session.query(User).filter_by(email="gautam@example.com").delete()
    db_session.commit()
    response = client.post(url, payload, format="json")
    
    assert response.status_code == 201
    assert response.data["message"] == "User created successfully"

    # Verify user exists in DB
    user = db_session.query(User).filter_by(email="gautam@example.com").first()
    assert user is not None
    assert user.name == "Gautam"




# import pytest
# from rest_framework.test import APIClient
# from employee_management.models.models import User, SessionLocal
# from sqlalchemy.exc import IntegrityError

# @pytest.fixture
# def client():
#     return APIClient()

# @pytest.fixture
# def db_session():
#     session = SessionLocal()
#     yield session
#     session.rollback()
#     session.close()

# @pytest.fixture
# def test_user(db_session):
#     """Creates a test user before running tests and cleans up afterward."""
#     user = User(name="Gautam", email="gautam@example.com", password="securepass")
#     db_session.add(user)
#     db_session.commit()
#     yield user
#     db_session.query(User).filter_by(email="gautam@example.com").delete()
#     db_session.commit()

# def test_create_user(client, db_session):
#     """Test successful user creation."""
#     url = "/users/"
#     payload = {"name": "Test User", "email": "test@example.com", "password": "securepass"}

#     response = client.post(url, payload, format="json")

#     assert response.status_code == 201
#     assert response.data["message"] == "User created successfully"
    
#     user = db_session.query(User).filter_by(email="test@example.com").first()
#     assert user is not None
#     assert user.name == "Test User"

# def test_create_user_missing_fields(client):
#     """Test creating a user with missing fields should return 400."""
#     url = "/users/"
#     payload = {"name": "Gautam"}
    
#     response = client.post(url, payload, format="json")
    
#     assert response.status_code == 400
#     assert "error" in response.data
#     assert "email" in str(response.data["error"])  # Convert to string for assertion

# def test_create_user_duplicate_email(client, test_user):
#     """Test creating a user with an existing email should return 400."""
#     url = "/users/"
#     payload = {"name": "Duplicate", "email": "gautam@example.com", "password": "securepass"}
    
#     response = client.post(url, payload, format="json")
    
#     assert response.status_code == 400
#     assert "error" in response.data
#     assert "Email already exists" in str(response.data["error"])  # Match error message

# def test_get_user(client, test_user):
#     """Test retrieving an existing user."""
#     url = f"/users/{test_user.email}/"
    
#     response = client.get(url)
    
#     assert response.status_code == 200
#     assert response.data["name"] == test_user.name

# def test_update_user(client, test_user):
#     """Test updating an existing user's name."""
#     url = f"/users/{test_user.email}/"
#     payload = {"name": "Updated Name"}
    
#     response = client.put(url, payload, format="json")
    
#     assert response.status_code == 200
#     assert "Updated Name" in str(response.data)  # Ensure the response contains the new name

# def test_delete_user(client, test_user, db_session):
#     """Test deleting an existing user."""
#     url = f"/users/{test_user.email}/"
    
#     response = client.delete(url)
    
#     assert response.status_code == 204  # No content
#     assert not db_session.query(User).filter_by(email=test_user.email).first()  # Ensure deleted
