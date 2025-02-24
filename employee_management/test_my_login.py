# import pytest
# from rest_framework.test import APIClient
# from rest_framework import status
# from unittest.mock import patch, MagicMock, call
# import bcrypt

# @pytest.fixture
# def api_client():
#     return APIClient()

# @pytest.fixture
# def mock_session():
#     with patch('employee_management.models.models.SessionLocal') as mock:
#         session = MagicMock()
#         mock.return_value.__enter__.return_value = session
#         mock.return_value.__exit__.return_value = None
#         yield session

# @pytest.fixture
# def mock_employee():
#     employee = MagicMock()
#     employee.employee_id = "EMP123"
#     employee.role = "user"
#     employee.is_active = True
#     employee.password = bcrypt.hashpw('test_password'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
#     return employee

# @pytest.fixture
# def mock_contact_details():
#     contact = MagicMock()
#     contact.email = "employee@company.com"
#     contact.employee_id = "EMP123"
#     return contact

# @pytest.mark.django_db
# class TestLoginView:
#     """Test suite for LoginView."""
    
#     def test_successful_login(self, api_client, mock_session, mock_employee):
#         """Test successful login without 2FA."""
#         login_url = '/login/'
#         login_data = {
#             'employee_id': 'EMP123',
#             'password': 'test_password',
#             'enable_2fa': False
#         }
        
#         mock_session.query.return_value.filter_by.return_value.first.return_value = mock_employee
#         mock_token = "mock_jwt_token"
        
#         with patch('employee_management.views.auth_views.generate_token', return_value=mock_token):
#             response = api_client.post(login_url, login_data, format='json')
            
#             assert response.status_code == status.HTTP_200_OK
#             assert response.data['success'] is True
#             assert response.data['message'] == 'Login successful'
#             assert response.data['enable_2fa'] is False
#             assert response.data['data']['token'] == mock_token
#             assert response.data['data']['employee_id'] == mock_employee.employee_id
#             assert response.data['data']['role'] == mock_employee.role
            
#             mock_session.commit.assert_called_once()

#     def test_successful_2fa_login(self, api_client, mock_session, mock_employee, mock_contact_details):
#         """Test successful login with 2FA enabled."""
#         login_url = '/login/'
#         login_data = {
#             'employee_id': 'EMP123',
#             'password': 'test_password',
#             'enable_2fa': True
#         }
        
#         mock_session.query.return_value.filter_by.return_value.first.side_effect = [
#             mock_employee,  # First call for employee
#             mock_contact_details  # Second call for contact details
#         ]
        
#         mock_otp = "123456"
#         with patch('employee_management.views.auth_views.generate_otp', return_value=mock_otp), \
#              patch('employee_management.views.auth_views.send_otp_email.delay') as mock_send_email:
            
#             response = api_client.post(login_url, login_data, format='json')
            
#             assert response.status_code == status.HTTP_200_OK
#             assert response.data['success'] is True
#             assert response.data['message'] == 'OTP sent to registered email'
#             assert response.data['enable_2fa'] is True
#             assert response.data['data']['employee_id'] == mock_employee.employee_id
#             assert response.data['data']['emp_email'] == mock_contact_details.email
            
#             mock_send_email.assert_called_once_with(mock_contact_details.email, mock_otp)
#             assert mock_session.commit.call_count == 2  # One for 2FA enable, one for OTP entry

#     def test_missing_credentials(self, api_client):
#         """Test login attempt with missing credentials."""
#         login_url = '/login/'
        
#         # Test missing password
#         response = api_client.post(login_url, {'employee_id': 'EMP123'}, format='json')
#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert response.data['success'] is False
        
#         # Test missing employee_id
#         response = api_client.post(login_url, {'password': 'test_password'}, format='json')
#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert response.data['success'] is False
        
#         # Test empty request
#         response = api_client.post(login_url, {}, format='json')
#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert response.data['success'] is False

#     def test_invalid_credentials(self, api_client, mock_session, mock_employee):
#         """Test login attempt with invalid credentials."""
#         login_url = '/login/'
#         login_data = {
#             'employee_id': 'EMP123',
#             'password': 'wrong_password',
#             'enable_2fa': False
#         }
        
#         mock_session.query.return_value.filter_by.return_value.first.return_value = mock_employee
        
#         response = api_client.post(login_url, login_data, format='json')
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#         assert response.data['success'] is False
#         assert response.data['message'] == 'Invalid credentials'

#     def test_inactive_employee(self, api_client, mock_session):
#         """Test login attempt for inactive employee."""
#         login_url = '/login/'
#         login_data = {
#             'employee_id': 'EMP123',
#             'password': 'test_password',
#             'enable_2fa': False
#         }
        
#         # Return None to simulate inactive or non-existent employee
#         mock_session.query.return_value.filter_by.return_value.first.return_value = None
        
#         response = api_client.post(login_url, login_data, format='json')
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#         assert response.data['success'] is False
#         assert response.data['message'] == 'Invalid credentials or inactive account'

#     def test_2fa_missing_contact_details(self, api_client, mock_session, mock_employee):
#         """Test 2FA login when contact details are missing."""
#         login_url = '/login/'
#         login_data = {
#             'employee_id': 'EMP123',
#             'password': 'test_password',
#             'enable_2fa': True
#         }
        
#         mock_session.query.return_value.filter_by.return_value.first.side_effect = [
#             mock_employee,  # First call for employee
#             None  # Second call for contact details (not found)
#         ]
        
#         with patch('employee_management.views.auth_views.generate_otp', return_value="123456"):
#             response = api_client.post(login_url, login_data, format='json')
            
#             assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
#             assert response.data['success'] is False
#             assert 'message' in response.data

#     def test_database_error(self, api_client, mock_session):
#         """Test handling of database errors during login."""
#         login_url = '/login/'
#         login_data = {
#             'employee_id': 'EMP123',
#             'password': 'test_password',
#             'enable_2fa': False
#         }
        
#         # Simulate database error
#         mock_session.query.side_effect = Exception("Database connection error")
        
#         response = api_client.post(login_url, login_data, format='json')
#         assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
#         assert response.data['success'] is False
#         assert 'message' in response.data

#     def test_token_generation_error(self, api_client, mock_session, mock_employee):
#         """Test handling of token generation errors."""
#         login_url = '/login/'
#         login_data = {
#             'employee_id': 'EMP123',
#             'password': 'test_password',
#             'enable_2fa': False
#         }
        
#         mock_session.query.return_value.filter_by.return_value.first.return_value = mock_employee
        
#         with patch('employee_management.views.auth_views.generate_token', 
#                   side_effect=Exception("Token generation failed")):
#             response = api_client.post(login_url, login_data, format='json')
            
#             assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
#             assert response.data['success'] is False
#             assert 'message' in response.data