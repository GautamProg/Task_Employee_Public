# import pytest
# from datetime import datetime, timedelta, timezone
# from unittest.mock import patch
# from django.urls import reverse
# from rest_framework.test import APIClient
# from rest_framework import status
# from employee_management.models.models import Employee, EmployeeOTP, SessionLocal

# from authentication.utils import generate_token  # Assuming generate_token is defined in utils

# @pytest.fixture
# def client():
#     return APIClient()

# @pytest.fixture
# def db_session():
#     session = SessionLocal()
#     yield session
#     session.close()

# @pytest.fixture
# def test_employee(db_session):
#     employee = Employee(employee_id="12345", is_active=True, role="admin")
#     db_session.add(employee)
#     db_session.commit()
#     return employee

# @pytest.fixture
# def valid_otp(test_employee, db_session):
#     otp_entry = EmployeeOTP(
#         emp_id=test_employee.employee_id,
#         otp="123456",
#         is_used=False,
#         is_expired=False,
#         created_on=datetime.now(timezone.utc) - timedelta(seconds=30)  # Valid OTP
#     )
#     db_session.add(otp_entry)
#     db_session.commit()
#     return otp_entry

# @pytest.fixture
# def expired_otp(test_employee, db_session):
#     otp_entry = EmployeeOTP(
#         emp_id=test_employee.employee_id,
#         otp="654321",
#         is_used=False,
#         is_expired=False,
#         created_on=datetime.now(timezone.utc) - timedelta(minutes=5)  # Expired OTP
#     )
#     db_session.add(otp_entry)
#     db_session.commit()
#     return otp_entry

# @patch("app.utils.generate_token", return_value="mocked_token")
# def test_verify_otp_success(mock_generate_token, client, test_employee, valid_otp):
#     response = client.post(reverse("verify_otp"), {"employee_id": test_employee.employee_id, "otp": "123456"})
#     assert response.status_code == status.HTTP_200_OK
#     assert response.data["success"] is True
#     assert response.data["data"]["token"] == "mocked_token"


# def test_verify_otp_missing_fields(client):
#     response = client.post(reverse("verify_otp"), {"employee_id": "12345"})
#     assert response.status_code == status.HTTP_400_BAD_REQUEST
#     assert response.data["success"] is False
#     assert "Employee ID and OTP are required" in response.data["message"]


# def test_verify_otp_invalid_employee(client):
#     response = client.post(reverse("verify_otp"), {"employee_id": "99999", "otp": "123456"})
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
#     assert response.data["success"] is False
#     assert "Invalid Employee ID or inactive account" in response.data["message"]


# def test_verify_otp_invalid_otp(client, test_employee):
#     response = client.post(reverse("verify_otp"), {"employee_id": test_employee.employee_id, "otp": "999999"})
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
#     assert response.data["success"] is False
#     assert "Invalid or expired OTP" in response.data["message"]


# def test_verify_otp_expired(client, test_employee, expired_otp):
#     response = client.post(reverse("verify_otp"), {"employee_id": test_employee.employee_id, "otp": "654321"})
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
#     assert response.data["success"] is False
#     assert "OTP has expired" in response.data["message"]
