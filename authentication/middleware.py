# authentication/middleware.py
from django.http import JsonResponse
from .utils import verify_token
# from sqlalchemy.orm import Session
from employee_management.models.models import Employee, SessionLocal

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Exclude login endpoint from authentication
        if request.path.endswith(('/login/', '/create/','/verifyOTP/', '/loginUI/', '/verify-otp/', '/dashboard/')):
            return self.get_response(request)

        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse(
                {'error': 'Authentication required'}, 
                status=401
            )

        token = auth_header.split(' ')[1]
        payload = verify_token(token)
        
        if not payload:
            return JsonResponse(
                {'error': 'Invalid or expired token'}, 
                status=401
            )

        # Add user information to request
        session = SessionLocal()
        try:
            employee = session.query(Employee).filter_by(
                employee_id=payload['employee_id']
            ).first()
            
            if not employee:
                return JsonResponse(
                    {'error': 'User not found'}, 
                    status=401
                )
                
            request.user = employee
            # request.user.role = employee.role  # Ensure role is accessible
            # request.user.employee_id = employee.employee_id  # Ensure employee_id is accessible
            # Add this in your middleware for debugging purposes:
            print(f"Authenticated user: {request.user}, role: {request.user.role}, employee_id: {request.user.employee_id}")

            return self.get_response(request)
        finally:
            session.close()