# import pytest
# from datetime import datetime, timezone
# from unittest.mock import Mock
# from rest_framework.test import APIRequestFactory
# from rest_framework import status

# from .views.auth_views import VerifyOTPView
# from .models.models import Employee, EmployeeOTP

# @pytest.fixture
# def mock_session():
#     session = Mock()
    
#     # Mock Employee query
#     employee = Mock()
#     employee.employee_id = "EMP202502080509232383"
#     employee.role = "employee"
#     employee.is_active = True
    
#     # Mock OTP entry
#     otp_entry = Mock()
#     otp_entry.emp_id = "EMP202502080509232383"
#     otp_entry.otp = "676274"
#     otp_entry.is_used = False
#     otp_entry.is_expired = False
#     otp_entry.created_on = datetime.now(timezone.utc)
    
#     # Configure session query mocks
#     session.query.return_value.filter_by.return_value.first.side_effect = [
#         employee,  # For Employee query
#         otp_entry  # For EmployeeOTP query
#     ]
#     session.query.return_value.filter_by.return_value.order_by.return_value.first.return_value = otp_entry
    
#     return session

# @pytest.fixture
# def mock_generate_token():
#     return Mock(return_value="mock_jwt_token")

# def test_verify_otp_success(monkeypatch, mock_session, mock_generate_token):
#     # Arrange
#     monkeypatch.setattr("your_app.views.SessionLocal", Mock(return_value=mock_session))
#     monkeypatch.setattr("your_app.views.generate_token", mock_generate_token)
    
#     factory = APIRequestFactory()
#     view = VerifyOTPView.as_view()
    
#     request_data = {
#         "employee_id": "EMP202502080509232383",
#         "otp": "d(:TD*wU2Qig"
#     }
    
#     request = factory.post('/verify-otp/', request_data, format='json')
    
#     # Act
#     response = view(request)
    
#     # Assert
#     assert response.status_code == status.HTTP_200_OK
#     assert response.data['success'] is True
#     assert response.data['message'] == 'OTP verified successfully'
#     assert response.data['data']['employee_id'] == "EMP202502080509232383"
#     assert response.data['data']['token'] == "mock_jwt_token"
#     assert response.data['data']['role'] == "employee"
    
#     # Verify OTP was marked as used
#     mock_session.commit.assert_called()