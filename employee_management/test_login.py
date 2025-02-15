# import pytest
# from django.urls import reverse
# from rest_framework.test import APIClient
# from faker import Faker
# from employee_management.models.models import Employee, SessionLocal # Import your model

# fake = Faker()

# @pytest.mark.django_db  # Use Django's test database
# def test_login_api():
#     client = APIClient()
#     session= SessionLocal()
#     employee_id = "EMP202502080616314793"
#     persisted_employee = session.query(Employee).filter_by(employee_id=employee_id).first()

#     if persisted_employee:
#         session.delete(persisted_employee)
#         session.commit()
#     # Create a test employee in the database
#     try:
#         employee = Employee(
#             employee_id="EMP202502080616314793",
#             employee_name="John Doe",
#             department="IT",
#             manager_id=None,  # Optional
#             salary=50000.0,  # Required
#             role="EMPLOYEE",
#             is_active=True,
#             password="$2b$12$CUuaBxNCRseHwCfnPW1uROKPMC0MTV8tRBmehfG83Rw12QDjBJhTm",  # Use an actual hashed password
#             two_fa_enabled=False
            
#         )
#         session.add(employee)
#         session.flush()
#         session.commit()

#         # Verify employee exists in DB
#         persisted_employee = session.query(Employee).filter_by(employee_id="EMP202502080616314793").first()
#         assert persisted_employee is not None, "Employee not found after commit!"

#         # Fake login data
#         data = {
#             "employee_id": "EMP202502080616314793",
#             "password": "W`/tY(N9EC2%",  # Change this to the correct password to test success
#             "enable_2fa": False
#         }

#         # Send a POST request to the login API
#         response = client.post(reverse("login"), data, format="json")

#         # Check response status
#         assert response.status_code in [200, 401]

#         if response.status_code == 200:
#             assert response.json()["success"] == True
#             assert "token" in response.json()["data"]  # Check if token exists
#         else:
#             assert response.json()["success"] == False

#     finally:
#         # Cleanup only if employee exists
#         if persisted_employee:
#             session.delete(persisted_employee)
#             session.commit()
        
#         session.expunge_all()  # Detach all instances
#         session.close() 








# import pytest
# from django.urls import reverse
# from rest_framework.test import APIClient
# from faker import Faker

# fake = Faker()

# @pytest.fixture
# def api_client():
#     return APIClient()

# @pytest.fixture
# def login_url():
#     return reverse('login')  # Adjust the endpoint name as per your Django URLs

# @pytest.fixture
# def valid_employee_data():
#     return {
#         "employee_id": fake.uuid4(),
#         "password": "Test@1234",
#         "enable_2fa": False
#     }

# @pytest.fixture
# def invalid_employee_data():
#     return {
#         "employee_id": fake.uuid4(),
#         "password": "WrongPass",
#         "enable_2fa": False
#     }

# @pytest.fixture
# def two_factor_employee_data():
#     return {
#         "employee_id": fake.uuid4(),
#         "password": "Test@1234",
#         "enable_2fa": True
#     }

# def test_login_success(api_client, login_url, valid_employee_data):
#     response = api_client.post(login_url, valid_employee_data, format='json')
#     assert response.status_code == 200
#     assert response.data["success"] is True
#     assert "token" in response.data["data"]

# def test_login_invalid_credentials(api_client, login_url, invalid_employee_data):
#     response = api_client.post(login_url, invalid_employee_data, format='json')
#     assert response.status_code == 401
#     assert response.data["success"] is False
#     assert response.data["message"] == "Invalid credentials"

# def test_login_missing_fields(api_client, login_url):
#     response = api_client.post(login_url, {}, format='json')
#     assert response.status_code == 400
#     assert response.data["success"] is False
#     assert response.data["message"] == "Employee ID and password are required"

# def test_login_with_2fa(api_client, login_url, two_factor_employee_data):
#     response = api_client.post(login_url, two_factor_employee_data, format='json')
#     assert response.status_code == 200
#     assert response.data["success"] is True
#     assert response.data["enable_2fa"] is True
#     assert "OTP sent to registered email" in response.data["message"]





# import pytest
# from django.urls import reverse
# from rest_framework.test import APIClient
# from faker import Faker
# from employee_management.models.models import Employee, SessionLocal
# import bcrypt

# fake = Faker()

# @pytest.mark.django_db
# def test_successful_login():
#     """Test successful login with correct credentials."""
#     client = APIClient()
#     session = SessionLocal()
    
#     # Generate test employee data
#     employee_id = fake.uuid4()[:10].upper()
#     password = "Test@1234"
#     hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

#     employee = Employee(
#         employee_id=employee_id,
#         employee_name=fake.name(),
#         department=fake.random_element(["IT", "HR", "Finance"]),
#         manager_id=None,
#         salary=50000.0,
#         role="EMPLOYEE",
#         is_active=True,
#         password=hashed_password,
#         two_fa_enabled=False
#     )

#     session.add(employee)
#     session.commit()

#     # API request
#     response = client.post(reverse("login"), {
#         "employee_id": employee_id,
#         "password": password,
#         "enable_2fa": False
#     }, format="json")

#     assert response.status_code == 200
#     assert response.json()["success"] is True
#     assert "token" in response.json()["data"]

#     session.delete(employee)
#     session.commit()
#     session.close()

# @pytest.mark.django_db
# def test_login_invalid_password():
#     """Test login with incorrect password."""
#     client = APIClient()
#     session = SessionLocal()

#     employee_id = fake.uuid4()[:10].upper()
#     correct_password = "CorrectPass123"
#     wrong_password = "WrongPass123"

#     hashed_password = bcrypt.hashpw(correct_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

#     employee = Employee(
#         employee_id=employee_id,
#         employee_name=fake.name(),
#         department="IT",
#         manager_id=None,
#         salary=60000.0,
#         role="EMPLOYEE",
#         is_active=True,
#         password=hashed_password,
#         two_fa_enabled=False
#     )

#     session.add(employee)
#     session.commit()

#     # API request
#     response = client.post(reverse("login"), {
#         "employee_id": employee_id,
#         "password": wrong_password,
#         "enable_2fa": False
#     }, format="json")

#     assert response.status_code == 401
#     assert response.json()["success"] is False
#     assert response.json()["message"] == "Invalid credentials"

#     session.delete(employee)
#     session.commit()
#     session.close()

# @pytest.mark.django_db
# def test_login_missing_fields():
#     """Test login with missing employee_id or password."""
#     client = APIClient()

#     # Missing password
#     response = client.post(reverse("login"), {
#         "employee_id": "EMP12345"
#     }, format="json")
#     assert response.status_code == 400
#     assert response.json()["success"] is False
#     assert response.json()["message"] == "Employee ID and password are required"

#     # Missing employee_id
#     response = client.post(reverse("login"), {
#         "password": "Test@1234"
#     }, format="json")
#     assert response.status_code == 400
#     assert response.json()["success"] is False
#     assert response.json()["message"] == "Employee ID and password are required"

# @pytest.mark.django_db
# def test_login_with_2fa_enabled():
#     """Test login when 2FA is enabled."""
#     client = APIClient()
#     session = SessionLocal()

#     employee_id = fake.uuid4()[:10].upper()
#     password = "SecurePass123"
#     hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

#     employee = Employee(
#         employee_id=employee_id,
#         employee_name=fake.name(),
#         department="IT",
#         manager_id=None,
#         salary=70000.0,
#         role="EMPLOYEE",
#         is_active=True,
#         password=hashed_password,
#         two_fa_enabled=True
#     )

#     session.add(employee)
#     session.commit()

#     response = client.post(reverse("login"), {
#         "employee_id": employee_id,
#         "password": password,
#         "enable_2fa": True
#     }, format="json")

#     assert response.status_code == 200
#     assert response.json()["success"] is True
#     assert response.json()["enable_2fa"] is True
#     assert "OTP sent to registered email" in response.json()["message"]

#     session.delete(employee)
#     session.commit()
#     session.close()


#pytest --ds=core.settings