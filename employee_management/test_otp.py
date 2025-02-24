# import pytest
# from unittest.mock import patch, MagicMock
# from datetime import datetime, timedelta, timezone
# from rest_framework.test import APIRequestFactory
# from rest_framework import status
# from django.test import RequestFactory
# from .models.models import Employee, EmployeeOTP
# from .views.auth_views import VerifyOTPView  # Replace 'your_module' with actual module name
# from authentication.utils import generate_token

# @pytest.fixture
# def factory():
#     return APIRequestFactory()

# @pytest.fixture
# def mock_session():
#     with patch("employee_management.models.models.SessionLocal") as mock:
#         yield mock()

# @pytest.fixture
# def mock_employee():
#     employee = MagicMock()
#     employee.employee_id = "EMP202502080509232383"
#     employee.role = "MANAGER"
#     return employee

# @pytest.fixture
# def mock_otp():
#     otp_entry = MagicMock()
#     otp_entry.created_on = datetime.now(timezone.utc) - timedelta(minutes=5)
#     otp_entry.is_used = False
#     otp_entry.is_expired = False
#     return otp_entry

# @patch("authentication.utils.generate_token", return_value="mock_token")
# # #this thing is working
# def test_verify_otp_success(mock_generate_token, factory, mock_session, mock_employee, mock_otp):
#     view = VerifyOTPView.as_view()
#     request = factory.post("/verify-otp/", {"employee_id": "EMP202502080509232383", "otp": "164365"}, format="json")
    
#     mock_session.query().filter_by().first.side_effect = [mock_employee, mock_otp]
#     response = view(request)
    
#     assert response.status_code == status.HTTP_200_OK
#     assert response.data["success"] is True
    #assert response.data["data"]["token"] == "mock_token"

# @patch("authentication.utils.generate_token", return_value="mock_token")
# def test_verify_otp_invalid_employee(mock_generate_token, factory, mock_session):
    
#     view = VerifyOTPView.as_view()
#     request = factory.post("/verify-otp/", {"employee_id": "EMP202502080509232382", "otp": "837099"}, format="json")
    
#     mock_session.query().filter_by().first.return_value = None
#     response = view(request)
#     print("Gautam testing",response.status_code)
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
#     print("Gautam testing",response.status_code)
#     assert response.data["success"] is False
#     print("Gautam testing",response.data)
#     assert response.data["message"] == "Invalid Employee ID or inactive account"


# @patch("authentication.utils.generate_token", return_value="mock_token")
# def test_verify_otp_expired(mock_generate_token, factory, mock_session, mock_employee, mock_otp):
#     view = VerifyOTPView.as_view()
#     request = factory.post("/verify-otp/", {"employee_id": "123", "otp": "456789"}, format="json")
    
#     mock_otp.created_on = datetime.now(timezone.utc) - timedelta(minutes=15)
#     mock_session.query().filter_by().first.side_effect = [mock_employee, mock_otp]
#     response = view(request)
    
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
#     assert response.data["success"] is False
#     assert response.data["message"] == "OTP has expired. Please request a new one."









import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models.models import Employee, SessionLocal


@pytest.mark.django_db
def test_get_employee_details_as_admin():
    client = APIClient()

    # Create a mock employee and admin user in the test database
    session = SessionLocal()
    admin_user = Employee(employee_id="EMP202502080509232382", employee_name="Kartavya", role="MANAGER")
    employee = Employee(employee_id="EMP202502080509232382", employee_name="Kartavya", department="IT", manager=None)
    
    session.add(admin_user)
    session.add(employee)
    session.commit()

    # Authenticate as admin
    client.force_authenticate(user=admin_user)

    # Make GET request
    url = reverse('employees', kwargs={"employee_id": "EMP202502080509232382"})
    response = client.get(url)

    # Assertions
    assert response.status_code == status.HTTP_200_OK
    assert response.data["success"] is True
    assert response.data["data"]["employee_details"]["employee_id"] == "EMP202502080509232382"
    assert response.data["data"]["employee_details"]["employee_name"] == "Kartavya"
    
    session.close()
























































# import pytest
# from unittest.mock import patch, MagicMock
# from django.urls import reverse
# from rest_framework.test import APIClient
# from datetime import datetime, timedelta, timezone
# from sqlalchemy.exc import IntegrityError
# from .models.models import Employee, EmployeeOTP  # Update with your actual app name
# from authentication.utils import generate_token  # Update with actual utility location

# @pytest.fixture
# def api_client():
#     """Fixture for API test client"""
#     return APIClient()

# @pytest.fixture
# def mock_session(mocker):
#     """Fixture for mocking SQLAlchemy session"""
#     return mocker.patch('employee_management.models.models.SessionLocal', autospec=True)

# @pytest.fixture
# def mock_employee():
#     """Fixture for mocking an active employee"""
#     employee = MagicMock(spec=Employee)
#     employee.employee_id = "EMP202502080509232383"
#     employee.is_active = True
#     employee.role = "MANAGER"
#     return employee

# @pytest.fixture
# def mock_valid_otp():
#     """Fixture for mocking a valid OTP entry"""
#     otp_entry = MagicMock(spec=EmployeeOTP)
#     otp_entry.otp = "266052"
#     otp_entry.is_used = False
#     otp_entry.is_expired = False
#     otp_entry.created_on = datetime.now(timezone.utc) - timedelta(minutes=5)  # Valid OTP
#     return otp_entry

# def test_verify_otp_success(api_client, mock_session, mock_employee, mock_valid_otp, mocker):
#     """Test successful OTP verification"""
#     mock_session_instance = mock_session.return_value
#     mock_session_instance.query().filter_by().first.side_effect = [mock_employee, mock_valid_otp]
    
#     mock_generate_token = mocker.patch('authentication.utils.generate_token', return_value="mock_token")
#     print("CHECKING",mock_generate_token);
#     response = api_client.post(reverse('verify-otp'), {"employee_id": "EMP202502080509232383", "otp": "266052"}, format='json')

#     assert response.status_code == 200
#     assert response.data['success'] is True
#     assert response.data['data']['token'] == "mock_token"

# def test_missing_employee_id_or_otp(api_client):
#     """Test missing employee_id or otp"""
#     response = api_client.post(reverse('verify-otp'), {"employee_id": "", "otp": ""}, format='json')
#     assert response.status_code == 400
#     assert response.data['message'] == "Employee ID and OTP are required"

# def test_invalid_employee_id(api_client, mock_session):
#     """Test invalid employee_id"""
#     mock_session_instance = mock_session.return_value
#     mock_session_instance.query().filter_by().first.return_value = None  # No employee found

#     response = api_client.post(reverse('verify-otp'), {"employee_id": "INVALID", "otp": "123456"}, format='json')

#     assert response.status_code == 401
#     assert response.data['message'] == "Invalid Employee ID or inactive account"

# def test_expired_otp(api_client, mock_session, mock_employee, mocker):
#     """Test expired OTP"""
#     expired_otp = MagicMock(spec=EmployeeOTP)
#     expired_otp.otp = "123456"
#     expired_otp.is_used = False
#     expired_otp.is_expired = False
#     expired_otp.created_on = datetime.now(timezone.utc) - timedelta(minutes=15)  # Expired OTP

#     mock_session_instance = mock_session.return_value
#     mock_session_instance.query().filter_by().first.side_effect = [mock_employee, expired_otp]

#     response = api_client.post(reverse('verify-otp'), {"employee_id": "EMP123", "otp": "123456"}, format='json')

#     assert response.status_code == 401
#     assert response.data['message'] == "OTP has expired. Please request a new one."

# def test_invalid_otp(api_client, mock_session, mock_employee):
#     """Test invalid OTP"""
#     mock_session_instance = mock_session.return_value
#     mock_session_instance.query().filter_by().first.side_effect = [mock_employee, None]  # No OTP found

#     response = api_client.post(reverse('verify-otp'), {"employee_id": "EMP123", "otp": "000000"}, format='json')

#     assert response.status_code == 401
#     assert response.data['message'] == "Invalid or expired OTP"

# def test_already_used_otp(api_client, mock_session, mock_employee):
#     """Test OTP already marked as used"""
#     used_otp = MagicMock(spec=EmployeeOTP)
#     used_otp.otp = "123456"
#     used_otp.is_used = True
#     used_otp.is_expired = False
#     used_otp.created_on = datetime.now(timezone.utc) - timedelta(minutes=5)

#     mock_session_instance = mock_session.return_value
#     mock_session_instance.query().filter_by().first.side_effect = [mock_employee, used_otp]

#     response = api_client.post(reverse('verify-otp'), {"employee_id": "EMP123", "otp": "123456"}, format='json')

#     assert response.status_code == 401
#     assert response.data['message'] == "Invalid or expired OTP"

# def test_token_generation_failure(api_client, mock_session, mock_employee, mock_valid_otp, mocker):
#     """Test failure in token generation"""
#     mock_session_instance = mock_session.return_value
#     mock_session_instance.query().filter_by().first.side_effect = [mock_employee, mock_valid_otp]

#     mocker.patch('authentication.utils.generate_token', side_effect=Exception("Token error"))

#     response = api_client.post(reverse('verify-otp'), {"employee_id": "EMP123", "otp": "123456"}, format='json')

#     assert response.status_code == 500
#     assert response.data['message'] == "Token generation failed. Try again later."

# def test_database_integrity_error(api_client, mock_session, mock_employee, mock_valid_otp):
#     """Test handling of database integrity error"""
#     mock_session_instance = mock_session.return_value
#     mock_session_instance.query().filter_by().first.side_effect = [mock_employee, mock_valid_otp]

#     mock_session_instance.commit.side_effect = IntegrityError("DB integrity error", None, None)

#     response = api_client.post(reverse('verify-otp'), {"employee_id": "EMP123", "otp": "123456"}, format='json')

#     assert response.status_code == 500
#     assert response.data['message'] == "Database integrity error. Please try again."

# def test_unexpected_exception(api_client, mock_session):
#     """Test handling of unexpected errors"""
#     mock_session_instance = mock_session.return_value
#     mock_session_instance.query().filter_by.side_effect = Exception("Unexpected error")

#     response = api_client.post(reverse('verify-otp'), {"employee_id": "EMP123", "otp": "123456"}, format='json')

#     assert response.status_code == 500
#     assert response.data['message'] == "An unexpected error occurred. Please try again later."


