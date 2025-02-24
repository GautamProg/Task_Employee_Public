# import pytest
# from rest_framework.test import APIClient
# from employee_management.models.models import User,SessionLocal, Employee
# from unittest.mock import patch, MagicMock

# @pytest.fixture
# def client():
#     return APIClient()

# @pytest.fixture
# def db_session():
#     session = SessionLocal()
#     yield session
#     session.rollback()  # Rollback after test execution
#     session.close()

# def test_create_user(client, db_session):
#     url = "/users/"  # Change this based on your actual URL
#     payload = {"name": "Gautam", "email": "gautam@example.com", "password": "securepass"}
    

#     db_session.query(User).filter_by(email="gautam@example.com").delete()
#     db_session.commit()
#     response = client.post(url, payload, format="json")
    
#     assert response.status_code == 201
#     assert response.data["message"] == "User created successfully"

#     # Verify user exists in DB
#     user = db_session.query(User).filter_by(email="gautam@example.com").first()
#     assert user is not None
#     assert user.name == "Gautam"



# @pytest.fixture
# def test_user(db_session):
#     user = Employee(employee_id="EMP202502080509232383", password="hashed_password", role="MANAGER")
#     db_session.add(user)
#     db_session.commit()
#     yield user
#     db_session.delete(user)
#     db_session.commit()

# @patch("employee_management.utils.generate_token", return_value="mocked_token")  # Mock token generation
# @patch("employee_management.utils.verify_password", return_value=True)  # Mock password verification
# @patch("employee_management.tasks.send_otp_email.delay")  # Mock Celery task

# def test_successful_login(mock_celery_task, mock_verify_password, mock_generate_token, client, db_session, test_user):
#     url = "/login/"  # Update this if needed
#     payload = {"employee_id": "EMP202502080509232383", "password": "d(:TD*wU2Qig"}

#     response = client.post(url, payload, format="json")
    
#     assert response.status_code == 200
#     assert response.data["success"] is True
#     assert response.data["message"] == "Login successful"
#     assert response.data["data"]["token"] == "mocked_token"







# import pytest
# from unittest.mock import patch, MagicMock
# from rest_framework.test import APIClient
# from .models.models import Employee, EmployeeOTP
# from datetime import datetime, timedelta, timezone
# from sqlalchemy.exc import IntegrityError, SQLAlchemyError

# @pytest.fixture
# def api_client():
#     return APIClient()

# @pytest.fixture
# def valid_employee():
#     return Employee(
#         employee_id="E123",
#         role="admin",
#         is_active=True
#     )

# @pytest.fixture
# def valid_otp():
#     return EmployeeOTP(
#         emp_id="E123",
#         otp="123456",
#         is_used=False,
#         is_expired=False,
#         created_on=datetime.now(timezone.utc) - timedelta(minutes=5)
#     )

# @pytest.mark.django_db
# class TestVerifyOTP:
    
#     @patch("authentication.utils.generate_token")
#     @patch("employee_management.views.auth_views.SessionLocal")
#     def test_verify_otp_success(self, mock_session, mock_generate_token, api_client, valid_employee, valid_otp):
#         # Create a new mock for each query chain
#         employee_query = MagicMock()
#         employee_query.first.return_value = valid_employee

#         otp_query = MagicMock()
#         otp_query.order_by.return_value.first.return_value = valid_otp

#         mock_db = MagicMock()
#         mock_session.return_value = mock_db

#         # Set up the query chain with different mock objects
#         def get_query_mock(*args, **kwargs):
#             if kwargs.get('employee_id') == 'E123' and kwargs.get('is_active', None) is True:
#                 return employee_query
#             return otp_query

#         mock_db.query.return_value.filter_by.side_effect = get_query_mock
        
#         # Ensure token generation returns exactly what we expect
#         mock_generate_token.return_value = "mocked_token"

#         response = api_client.post("/verifyOTP/", {"employee_id": "E123", "otp": "123456"})

#         # Verify that generate_token was called with correct parameters
#         mock_generate_token.assert_called_once_with(valid_employee.employee_id, valid_employee.role)

#         assert response.status_code == 200
#         response_data = response.json()
#         assert response_data["success"] is True
#         assert response_data["message"] == "OTP verified successfully"
#         assert response_data["data"]["employee_id"] == "E123"
#         assert response_data["data"]["role"] == "admin"
#         assert "token" in response_data["data"]

#     @patch("authentication.utils.generate_token")
#     @patch("employee_management.views.auth_views.SessionLocal")
#     def test_verify_otp_token_failure(self, mock_session, mock_generate_token, api_client, valid_employee, valid_otp):
#         # Create separate mocks for different queries
#         employee_query = MagicMock()
#         employee_query.first.return_value = valid_employee

#         otp_query = MagicMock()
#         otp_query.order_by.return_value.first.return_value = valid_otp

#         mock_db = MagicMock()
#         mock_session.return_value = mock_db

#         # Set up the query chain
#         def get_query_mock(*args, **kwargs):
#             if kwargs.get('employee_id') == 'E123' and kwargs.get('is_active', None) is True:
#                 return employee_query
#             return otp_query

#         mock_db.query.return_value.filter_by.side_effect = get_query_mock

#         # Ensure token generation raises an exception
#         mock_generate_token.side_effect = Exception("Token generation failed")

#         response = api_client.post("/verifyOTP/", {"employee_id": "E123", "otp": "123456"})

#         assert response.status_code == 500
#         assert response.json() == {
#             "success": False,
#             "message": "Token generation failed. Try again later."
#         }

#     @patch("employee_management.views.auth_views.SessionLocal")
#     def test_verify_otp_invalid_employee(self, mock_session, api_client):
#         mock_db = MagicMock()
#         mock_session.return_value = mock_db
        
#         # Mock employee query to return None
#         mock_db.query.return_value.filter_by.return_value.first.return_value = None

#         response = api_client.post("/verifyOTP/", {"employee_id": "E123", "otp": "123456"})

#         assert response.status_code == 401
#         assert response.json() == {
#             "success": False,
#             "message": "Invalid Employee ID or inactive account"
#         }

#     @patch("employee_management.views.auth_views.SessionLocal")
#     def test_verify_otp_invalid_or_expired(self, mock_session, api_client, valid_employee):
#         # Create separate mocks for different queries
#         employee_query = MagicMock()
#         employee_query.first.return_value = valid_employee

#         otp_query = MagicMock()
#         otp_query.order_by.return_value.first.return_value = None

#         mock_db = MagicMock()
#         mock_session.return_value = mock_db

#         # Set up the query chain
#         def get_query_mock(*args, **kwargs):
#             if kwargs.get('employee_id') == 'E123' and kwargs.get('is_active', None) is True:
#                 return employee_query
#             return otp_query

#         mock_db.query.return_value.filter_by.side_effect = get_query_mock

#         response = api_client.post("/verifyOTP/", {"employee_id": "E123", "otp": "wrong_otp"})

#         assert response.status_code == 401
#         assert response.json() == {
#             "success": False,
#             "message": "Invalid or expired OTP"
#         }

#     @patch("employee_management.views.auth_views.SessionLocal")
#     def test_verify_otp_expired(self, mock_session, api_client, valid_employee):
#         # Create separate mocks for different queries
#         employee_query = MagicMock()
#         employee_query.first.return_value = valid_employee

#         expired_otp = EmployeeOTP(
#             emp_id="E123",
#             otp="123456",
#             is_used=False,
#             is_expired=False,
#             created_on=datetime.now(timezone.utc) - timedelta(minutes=15)
#         )

#         otp_query = MagicMock()
#         otp_query.order_by.return_value.first.return_value = expired_otp

#         mock_db = MagicMock()
#         mock_session.return_value = mock_db

#         # Set up the query chain
#         def get_query_mock(*args, **kwargs):
#             if kwargs.get('employee_id') == 'E123' and kwargs.get('is_active', None) is True:
#                 return employee_query
#             return otp_query

#         mock_db.query.return_value.filter_by.side_effect = get_query_mock

#         response = api_client.post("/verifyOTP/", {"employee_id": "E123", "otp": "123456"})

#         assert response.status_code == 401
#         assert response.json() == {
#             "success": False,
#             "message": "OTP has expired. Please request a new one."
#         }
