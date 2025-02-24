import pytest
from unittest.mock import patch, MagicMock
from rest_framework.test import APIClient
from .models.models import Employee, EmployeeOTP
from datetime import datetime, timedelta, timezone
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


@pytest.mark.django_db
@patch("authentication.utils.generate_token")  # Mock token generation
@patch("employee_management.models.models.SessionLocal")  # Mock SQLAlchemy session
def test_verify_otp_success(mock_session, mock_generate_token):
    client = APIClient()
    
    # Mock database session
    mock_db = MagicMock()
    mock_session.return_value = mock_db

    # Mock employee
    mock_employee = Employee(employee_id="E123", role="admin", is_active=True)
    mock_db.query.return_value.filter_by.return_value.first.side_effect = [mock_employee]

    # Mock valid OTP entry
    mock_otp = EmployeeOTP(
        emp_id="E123",
        otp="123456",
        is_used=False,
        is_expired=False,
        created_on=datetime.now(timezone.utc) - timedelta(minutes=5)
    )
    mock_db.query.return_value.filter_by.return_value.order_by.return_value.first.return_value = mock_otp

    # Mock token generation
    mock_generate_token.return_value = "mocked_token"

    # Simulate API call
    response = client.post("/verifyOTP/", {"employee_id": "E123", "otp": "123456"})
    print("Gautam Testing", response.json(), response.status_code)
    # Assertions
    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "message": "OTP verified successfully",
        "data": {
            "token": "mocked_token",
            "employee_id": "E123",
            "role": "admin"
        }
    }



@pytest.mark.django_db
@patch("employee_management.models.models.SessionLocal")
def test_verify_otp_invalid_employee(mock_session):
    client = APIClient()
    
    mock_db = MagicMock()
    mock_session.return_value = mock_db

    mock_db.query.return_value.filter_by.return_value.first.side_effect = [None]
    response = client.post("/verifyOTP/", {"employee_id": "E123", "otp": "123456"})
    print( "Gautam is testing1",response.json()) 
    assert response.status_code == 401
    assert response.json() == {"success": False, "message": "Invalid Employee ID or inactive account"}



# @pytest.mark.django_db
# @patch("employee_management.views.auth_views.SessionLocal")
# def test_verify_otp_invalid_or_expired(mock_session):
#     client = APIClient()

#     mock_db = MagicMock()
#     mock_session.return_value = mock_db

#     # Mock employee query (Valid Employee)
#     mock_query = MagicMock()
#     mock_db.query.return_value.filter_by.return_value = mock_query  # Fix order_by() error
#     mock_query.order_by.return_value.first.return_value = None  # Simulate no OTP found



#     # Mock active employee
#     mock_employee = Employee(employee_id="E123", is_active=True)
#     mock_db.query.return_value.filter_by.return_value.first.side_effect = [mock_employee, None]

#     response = client.post("/verifyOTP/", {"employee_id": "E123", "otp": "wrong_otp"})
#     print( "Gautam is testing2",response.json()) 
#     assert response.status_code == 401
#     assert response.json() == {"success": False, "message": "Invalid or expired OTP"}






# @pytest.mark.django_db
# @patch("employee_management.models.models.SessionLocal")
# def test_verify_otp_expired(mock_session):
#     client = APIClient()

#     mock_db = MagicMock()
#     mock_session.return_value = mock_db

#     mock_employee = Employee(employee_id="E123", is_active=True)
#     mock_db.query.return_value.filter_by.return_value.first.side_effect = [mock_employee]

#     expired_otp = EmployeeOTP(
#         emp_id="E123",
#         otp="123456",
#         is_used=False,
#         is_expired=False,
#         created_on=datetime.now(timezone.utc) - timedelta(minutes=15)  # Expired OTP
#     )
#     mock_db.query.return_value.filter_by.return_value.order_by.return_value.first.return_value = expired_otp

#     response = client.post("/verifyOTP/", {"employee_id": "E123", "otp": "123456"})

#     assert response.status_code == 401
#     assert response.json() == {"success": False, "message": "OTP has expired. Please request a new one."}






# @pytest.mark.django_db
# @patch("authentication.utils.generate_token", side_effect=Exception("Token Error"))  # Simulate token failure
# @patch("employee_management.models.models.SessionLocal")
# def test_verify_otp_token_failure(mock_session, mock_generate_token):
#     client = APIClient()

#     mock_db = MagicMock()
#     mock_session.return_value = mock_db

#     mock_employee = Employee(employee_id="E123", role="admin", is_active=True)
#     mock_db.query.return_value.filter_by.return_value.first.side_effect = [mock_employee]

#     mock_otp = EmployeeOTP(
#         emp_id="E123",
#         otp="123456",
#         is_used=False,
#         is_expired=False,
#         created_on=datetime.now(timezone.utc) - timedelta(minutes=5)
#     )
#     mock_db.query.return_value.filter_by.return_value.order_by.return_value.first.return_value = mock_otp

#     response = client.post("/verifyOTP/", {"employee_id": "E123", "otp": "123456"})
#     print("Gautam Testing", response.json(), response.status_code)

#     assert response.status_code == 500
#     assert response.json() == {"success": False, "message": "Token generation failed. Try again later."}














