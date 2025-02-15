# employee_management/views/auth_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from ..models.models import Employee, SessionLocal, EmployeeOTP, ContactDetails
from authentication.utils import generate_token, generate_otp, get_employee_from_cache, cache_otp, get_cached_otp
import bcrypt
from employee_management.tasks import send_otp_email
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class LoginView(APIView):
    """Handle employee login and token generation."""
    
    def post(self, request):
        employee_id = request.data.get('employee_id')
        password = request.data.get('password')
        twoFactorValue= request.data.get('enable_2fa')

        if not employee_id or not password:
            return Response(
                {
                    'success': False,
                    'message': 'Employee ID and password are required'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        session = SessionLocal()
        try:
                employee = session.query(Employee).filter_by(
                    employee_id=employee_id,
                    is_active=True
                ).first()
                #employee = get_employee_from_cache(employee_id)
                
                if not employee:
                    return Response(
                        {
                            'success': False,
                            'message': 'Invalid credentials or inactive account'
                        },
                        status=status.HTTP_401_UNAUTHORIZED
                    )
                
                # Verify password
                if not bcrypt.checkpw(
                    password.encode('utf-8'), 
                    employee.password.encode('utf-8')
                ):
                
                    return Response(
                        {
                            'success': False,
                            'message': 'Invalid credentials'
                        },
                        status=status.HTTP_401_UNAUTHORIZED
                    )
                
                if twoFactorValue:
                    otp = generate_otp()
                    employee.two_fa_enabled=True
                    print("DONE DONE DONE DONE")
                    session.commit()

                    # Store OTP in database
                    otp_entry = EmployeeOTP(
                    emp_id=employee.employee_id,
                    otp=otp,
                    is_used=False,
                    is_expired=False
                    )
                    session.add(otp_entry)
                    session.commit()

                    contact= session.query(ContactDetails).filter_by(employee_id=employee.employee_id).first()
                    email=contact.email
                    send_otp_email.delay(email, otp)
                    # send_mail(
                    #     'Hurray! you have enabled 2FA.Your Login OTP',
                    #     f'Your OTP for login is {otp}. It is valid for just one use.',
                    #     'noreply@company.com',
                    #     [email],  # Assuming `email` field exists in Employee model
                    #     fail_silently=False,
                    #     )

                    return Response({
                            'success': True,
                            'message': 'OTP sent to registered email',
                            'enable_2fa': True,
                            '2FactorAuthentication': 'Congrats! 2FA enabled',
                            'data': {
                                'employee_id': employee.employee_id,
                                'emp_email': email
                            }
                        })
                    
                else:
                    # Generate token
                    employee.two_fa_enabled= False
                    session.commit()
                    token = generate_token(employee.employee_id, employee.role)
                    
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(
                    "login_updates",
                    {
                        "type": "send_login_update",
                        "message": {
                            "employee_id": employee.employee_id,
                            "message": f"{employee.employee_name} has logged in!"
                        }
                    }
                )

                    
                    print("2FA Disabled")
                    return Response({
                        'success': True,
                        'message': 'Login successful',
                        'enable_2fa': False,
                        'data': {
                            'token': token,
                            'employee_id': employee.employee_id,
                            'role': employee.role
                        }
                    })
        except Exception as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        finally:
            session.close()











class VerifyOTPView(APIView):
    """Verify OTP and provide authentication token."""

    def post(self, request):
        

        employee_id = request.data.get('employee_id')
        otp = request.data.get('otp')

        if not employee_id or not otp:
            return Response(
                {
                    'success': False,
                    'message': 'Employee ID and OTP are required'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        session = SessionLocal()
        try:
            # Fetch employee
            employee = session.query(Employee).filter_by(
                employee_id=employee_id,
                is_active=True
            ).first()

            if not employee:
                return Response(
                    {
                        'success': False,
                        'message': 'Invalid Employee ID or inactive account'
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Fetch latest OTP for the employee
            otp_entry = session.query(EmployeeOTP).filter_by(
                emp_id=employee_id,
                otp=otp,
                is_used=False,
                is_expired=False
            ).order_by(EmployeeOTP.created_on.desc()).first()
            
            
            if not otp_entry:
                return Response(
                    {
                        'success': False,
                        'message': 'Invalid or expired OTP'
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )

            #Check if OTP is expired (valid for 10 minutes)
            otp_expiry_time = otp_entry.created_on + timedelta(minutes=1)
            if datetime.now(timezone.utc) > otp_expiry_time.replace(tzinfo=timezone.utc):
                otp_entry.is_expired = True
                session.commit()
                return Response(
                    {
                        'success': False,
                        'message': 'OTP has expired. Please request a new one.'
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )


            # otp_created_time = otp_entry.created_on
            # if otp_created_time.tzinfo is None:
            #     otp_created_time = otp_created_time.replace(tzinfo=timezone.utc)

            # # Check if OTP is expired (valid for 1 minute)
            # otp_expiry_time = otp_created_time + timedelta(minutes=1)

            # if datetime.now(timezone.utc) > otp_expiry_time:
            #     otp_entry.is_expired = True
            #     session.commit()
            #     return Response(
            #         {'success': False, 'message': 'OTP has expired. Please request a new one.'},
            #         status=status.HTTP_401_UNAUTHORIZED
            #     )

            # Mark OTP as used
            otp_entry.is_used = True
            session.commit()

            # Generate token
            token = generate_token(employee.employee_id, employee.role)
           

            return Response({
                'success': True,
                'message': 'OTP verified successfully',
                'data': {
                    'token': token,
                    'employee_id': employee.employee_id,
                    'role': employee.role
                }
            })
        except Exception as e:
            session.rollback()
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        finally:
            session.close()





# Manager: Kartavya Login Credentials:

# "employee_id": "EMP202502080509232383",
# "password": "d(:TD*wU2Qig",