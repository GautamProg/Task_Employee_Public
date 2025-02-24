# import pytest
# import bcrypt
# from unittest.mock import patch, MagicMock
# from rest_framework.test import APIClient
# from .models.models import Employee, EmployeeOTP, ContactDetails
# from authentication.utils import generate_token

# @pytest.mark.django_db
# @patch("authentication.utils.generate_token")  # Mock token generation
# @patch("employee_management.models.models.SessionLocal")  # Mock database session
# def test_login_success(mock_session, mock_generate_token):
#     client = APIClient()

#     # Mock database session
#     mock_db = MagicMock()
#     mock_session.return_value = mock_db

#     # Mock employee
#     hashed_password = bcrypt.hashpw("correct_password".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
#     mock_employee = Employee(employee_id="E123", password=hashed_password, role="admin", is_active=True)
#     mock_contact = ContactDetails(employee_id="E123", email="test@example.com")
#    # mock_db.query.return_value.filter_by.return_value.first.return_value = mock_employee
     

#     def mock_filter_by(**kwargs):
#         if kwargs.get("employee_id") == "E123":
#             return MagicMock(first=lambda: mock_employee)
#         return MagicMock(first=lambda: None)

#     mock_db.query.return_value.filter_by.side_effect = mock_filter_by
#     mock_db.query(ContactDetails).filter_by.return_value.first.return_value = mock_contact


#     # Mock token generation
#     mock_generate_token.return_value = "mocked_token"
#     print("newToken", mock_generate_token)

#     # Simulate API call
#     response = client.post("/login/", {"employee_id": "E123", "password": "correct_password", "enable_2fa": False})
#     print("meTESTING", response.json(), response.status_code)
#     assert response.status_code == 200
#     assert response.json() == {
#         "success": True,
#         "message": "Login successful",
#         "enable_2fa": False,
#         "data": {
#             "token": "mocked_token",
#             "employee_id": "E123",
#             "role": "admin"
#         }
#     }






# @pytest.mark.django_db
# @patch("employee_management.models.models.SessionLocal")
# def test_login_invalid_credentials(mock_session):
#     client = APIClient()

#     # Mock database session
#     mock_db = MagicMock()
#     mock_session.return_value = mock_db

#     # Employee does not exist
#     mock_db.query.return_value.filter_by.return_value.first.return_value = None

#     response = client.post("/login/", {"employee_id": "E123", "password": "wrong_password"})
    
#     assert response.status_code == 401
#     assert response.json() == {"success": False, "message": "Invalid credentials or inactive account"}




# @pytest.mark.django_db
# @patch("authentication.utils.generate_token")
# @patch("employee_management.models.models.SessionLocal")
# def test_login_2fa_enabled(mock_session, mock_generate_token):
#     client = APIClient()

#     mock_db = MagicMock()
#     mock_session.return_value = mock_db

#     hashed_password = bcrypt.hashpw("correct_password".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
#     mock_employee = Employee(employee_id="E123", password=hashed_password, role="admin", is_active=True)

#     mock_db.query.return_value.filter_by.return_value.first.return_value = mock_employee

#     # Mock email retrieval
#     mock_contact = ContactDetails(employee_id="E123", email="test@example.com")
#     mock_db.query.return_value.filter_by.return_value.first.side_effect = [mock_employee, mock_contact]

#     # Simulate API call with 2FA enabled
#     response = client.post("/login/", {"employee_id": "E123", "password": "correct_password", "enable_2fa": True})
#     print("Gautam testing", response.json(), "StatusCode", response.status_code)
#     assert response.status_code == 200
#     assert response.json() == {
#         "success": True,
#         "message": "OTP sent to registered email",
#         "enable_2fa": True,
#         "2FactorAuthentication": "Congrats! 2FA enabled",
#         "data": {
#             "employee_id": "E123",
#             "emp_email": "test@example.com"
#         }
#     }




# @pytest.mark.django_db
# @patch("employee_management.models.models.SessionLocal")
# def test_login_missing_credentials(mock_session):
#     client = APIClient()

#     response = client.post("/login/", {"employee_id": "", "password": ""})
    
#     assert response.status_code == 400
#     assert response.json() == {"success": False, "message": "Employee ID and password are required"}




# @pytest.mark.django_db
# @patch("authentication.utils.generate_token", side_effect=Exception("Token Error"))
# @patch("employee_management.models.models.ContactDetails")
# @patch("employee_management.models.models.SessionLocal")
# def test_login_token_failure(mock_session, mock_generate_token, mock_contact_details):
#     client = APIClient()

#     mock_db = MagicMock()
#     mock_session.return_value = mock_db

#     hashed_password = bcrypt.hashpw("correct_password".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
#     mock_employee = Employee(employee_id="E123", password=hashed_password, role="admin", is_active=True)

#     mock_contact = MagicMock()
#     mock_contact.email = "test@example.com"
#     mock_contact_details.query.return_value.filter_by.return_value.first.return_value = mock_contact
#     mock_db.query.return_value.filter_by.return_value.first.return_value = mock_employee
#     response = client.post("/login/", {"employee_id": "E123", "password": "correct_password", "enable_2fa": False})
#     print("meTESTING", response.json())
#     assert response.status_code == 500
#     assert response.json() == {"success": False, "message": "Token Error"}









# this is the one given by claude ai
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock
import bcrypt

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def mock_session():
    with patch('employee_management.models.models.SessionLocal') as mock:
        session = MagicMock()
        mock.return_value.__enter__.return_value = session
        mock.return_value.__exit__.return_value = None
        yield session

@pytest.fixture
def mock_employee():
    employee = MagicMock()
    employee.employee_id = "EMP123"
    employee.role = "user"
    employee.is_active = True
    # Hash a test password
    employee.password = bcrypt.hashpw('test_password'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    return employee

@pytest.mark.django_db
def test_successful_login(api_client, mock_session, mock_employee):
    # Arrange
    login_url = '/login/'  # Update with your actual login URL
    login_data = {
        'employee_id': 'EMP123',
        'password': 'test_password',
        'enable_2fa': False
    }
    
    # Mock the database query
    mock_session.query.return_value.filter_by.return_value.first.return_value = mock_employee
    
    # Mock token generation
    mock_token = "mock_jwt_token"
    with patch('authentication.utils.generate_token', return_value=mock_token):
        # Act
        response = api_client.post(login_url, login_data, format='json')
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data['success'] is True
        assert response.data['message'] == 'Login successful'
        assert response.data['enable_2fa'] is False
        print("myToken", response.json())
        assert response.data['data']['token'] == mock_token
        assert response.data['data']['employee_id'] == mock_employee.employee_id
        assert response.data['data']['role'] == mock_employee.role
        
        # Verify session interactions
        mock_session.query.assert_called_once()
        mock_session.commit.assert_called_once()






# ✅ **Test Case 2: Login with Invalid Password**
@pytest.mark.django_db
def test_invalid_password(api_client, mock_session, mock_employee):
    login_url = '/login/'
    login_data = {
        'employee_id': 'EMP123',
        'password': 'wrong_password',
        'enable_2fa': False
    }

    mock_session.query.return_value.filter_by.return_value.first.return_value = mock_employee

    with patch('bcrypt.checkpw', return_value=False):
        response = api_client.post(login_url, login_data, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data['success'] is False
        assert response.data['message'] == 'Invalid credentials'




# ✅ **Test Case 3: Login with Non-Existent Employee**
# @pytest.mark.django_db
# def test_non_existent_employee(api_client, mock_session):
#     login_url = '/login/'
#     login_data = {
#         'employee_id': 'NON_EXISTENT',
#         'password': 'test_password',
#         'enable_2fa': False
#     }

#     mock_session.query.return_value.filter_by.return_value.first.return_value = None

#     response = api_client.post(login_url, login_data, format='json')

#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
#     assert response.data['success'] is False
#     assert response.data['message'] == 'Invalid credentials or inactive account'





# ✅ **Test Case 4: Login with Missing Fields**
@pytest.mark.django_db
@pytest.mark.parametrize("login_data, expected_message", [
    ({'password': 'test_password'}, "Employee ID and password are required"),
    ({'employee_id': 'EMP123'}, "Employee ID and password are required"),
    ({}, "Employee ID and password are required"),
])
def test_missing_fields(api_client, login_data, expected_message):
    login_url = '/login/'

    response = api_client.post(login_url, login_data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['success'] is False
    assert response.data['message'] == expected_message






# ✅ **Test Case 5: Login with 2FA Enabled**
# @pytest.mark.django_db
# def test_login_with_2fa(api_client, mock_session, mock_employee):
#     login_url = '/login/'
#     login_data = {
#         'employee_id': 'EMP123',
#         'password': 'test_password',
#         'enable_2fa': True
#     }

#     mock_session.query.return_value.filter_by.return_value.first.return_value = mock_employee

#     with patch('authentication.utils.generate_otp', return_value="123456"), \
#          patch('employee_management.models.models.ContactDetails') as mock_contact, \
#          patch('authentication.utils.send_otp_email') as mock_email_sender:

#         mock_contact_instance = MagicMock()
#         mock_contact_instance.email = "test@example.com"
#         mock_session.query.return_value.filter_by.return_value.first.return_value = mock_contact_instance

#         response = api_client.post(login_url, login_data, format='json')

#         assert response.status_code == status.HTTP_200_OK
#         assert response.data['success'] is True
#         assert response.data['enable_2fa'] is True
#         assert response.data['message'] == 'OTP sent to registered email'
#         assert response.data['data']['employee_id'] == mock_employee.employee_id
#         assert response.data['data']['emp_email'] == "test@example.com"

#         mock_email_sender.delay.assert_called_once_with("test@example.com", "123456")
#         mock_session.commit.assert_called()




# ✅ **Test Case 6: Login with 2FA Enabled but No Email Found**
@pytest.mark.django_db
def test_login_with_2fa_no_email(api_client, mock_session, mock_employee):
    login_url = '/login/'
    login_data = {
        'employee_id': 'EMP123',
        'password': 'test_password',
        'enable_2fa': True
    }

    mock_session.query.return_value.filter_by.return_value.first.return_value = mock_employee
    mock_session.query.return_value.filter_by.return_value.first.return_value = None  # No contact details found

    response = api_client.post(login_url, login_data, format='json')

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.data['success'] is False





