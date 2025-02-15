# employee_management/urls.py
from django.urls import path
from .views.views import EmployeeCreateView, EmployeeDetailView, UserCreateAPIView
from .views.auth_views import LoginView, VerifyOTPView
from employee_management.views.views import login_view, verify_otp_view, dashboard_view, ws_view

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('employees/create/', EmployeeCreateView.as_view(), name='employee-create'),
    path('employees/<str:employee_id>/', EmployeeDetailView.as_view(), name='employee-detail'),
    path('verifyOTP/', VerifyOTPView.as_view(), name='verify-otp'),
    path('loginUI/', login_view, name='login'),
    path('verify-otp/', verify_otp_view, name='verify-otp'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path("users/", UserCreateAPIView.as_view(), name="user-create"),
    path('wsUI/', ws_view, name='ws_UI'),

]