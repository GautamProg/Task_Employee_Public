import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from unittest.mock import patch, MagicMock
from employee_management.models.models import Employee

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def mock_session():
    with patch('employee_management.models.models.SessionLocal') as mock:
        session = MagicMock()
        mock.return_value = session
        yield session

@pytest.fixture
def mock_verify_token():
    with patch('authentication.middleware.verify_token') as mock:
        yield mock

@pytest.fixture
def mock_employee():
    employee = MagicMock(spec=Employee)
    employee.employee_id = "EMP123"
    employee.employee_name = "John Doe"
    employee.department = "Engineering"
    employee.role = "EMPLOYEE"
    employee.manager = MagicMock()
    employee.manager.employee_id = "MGR456"
    employee.manager.employee_name = "Jane Manager"
    return employee

@pytest.mark.django_db
class TestEmployeeDetailView:
    def test_get_employee_details_as_admin(self, api_client, mock_session, mock_employee, mock_verify_token):
        """
        Test case 1: Admin user retrieving employee details
        Should return 200 with employee data
        """
        # Arrange
        admin_employee = MagicMock(spec=Employee)
        admin_employee.employee_id = "ADMIN789"
        admin_employee.role = "ADMIN"
        
        # Mock the token verification
        mock_verify_token.return_value = {"employee_id": "ADMIN789"}
        
        # Mock the session query for middleware
        mock_session.query.return_value.filter_by.return_value.first.side_effect = [
            admin_employee,  # First call for middleware authentication
            mock_employee   # Second call for actual view query
        ]
        
        # Set JWT token in header
        api_client.credentials(HTTP_AUTHORIZATION='Bearer dummy-token')
        
        # Act
        url = reverse('employee-detail', kwargs={'employee_id': 'EMP123'})
        response = api_client.get(url)
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data['success'] is True
        assert response.data['data']['employee_details']['employee_id'] == 'EMP123'

    def test_get_employee_details_as_employee_self(self, api_client, mock_session, mock_employee, mock_verify_token):
        """
        Test case 2: Employee retrieving their own details
        Should return 200 with employee data
        """
        # Arrange
        mock_verify_token.return_value = {"employee_id": "EMP123"}
        
        # Set up mock to return the same employee for both queries
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_first = MagicMock()
        
        mock_session.query.return_value = mock_query
        mock_query.filter_by.return_value = mock_filter
        mock_filter.first.side_effect = [mock_employee, mock_employee]
        
        api_client.credentials(HTTP_AUTHORIZATION='Bearer dummy-token')
        
        # Act
        url = reverse('employee-detail', kwargs={'employee_id': 'EMP123'})
        response = api_client.get(url)
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data['success'] is True
        assert response.data['data']['employee_details']['employee_id'] == 'EMP123'

    def test_get_employee_details_as_employee_unauthorized(self, api_client, mock_session, mock_employee, mock_verify_token):
        """
        Test case 3: Employee trying to access another employee's details
        Should return 403 Forbidden
        """
        # Arrange
        unauthorized_employee = MagicMock(spec=Employee)
        unauthorized_employee.employee_id = "EMP999"
        unauthorized_employee.role = "EMPLOYEE"
        
        mock_verify_token.return_value = {"employee_id": "EMP999"}
        
        # Set up mock to return different values for each query
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_first = MagicMock()
        
        mock_session.query.return_value = mock_query
        mock_query.filter_by.return_value = mock_filter
        mock_filter.first.side_effect = [unauthorized_employee, mock_employee]
        
        api_client.credentials(HTTP_AUTHORIZATION='Bearer dummy-token')
        
        # Act
        url = reverse('employee-detail', kwargs={'employee_id': 'EMP123'})
        response = api_client.get(url)
        
        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data['success'] is False
        assert response.data['message'] == 'Permission denied'