# employee_management/views/auth_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from ..models.models import Employee, SessionLocal, EmployeeOTP, ContactDetails
from authentication.utils import generate_token, generate_otp, get_employee_from_cache, cache_otp, get_cached_otp
import bcrypt
from employee_management.tasks import send_otp_email
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import logging

logger = logging.getLogger('core')



# class LoginView(APIView):
#     """Handle employee login and token generation."""
    
#     def post(self, request):
#         employee_id = request.data.get('employee_id')
#         password = request.data.get('password')
#         twoFactorValue= request.data.get('enable_2fa')
#         logger.debug("Login attempt started for employee_id: %s", employee_id)
#         if not employee_id or not password:
#             logger.warning("Employee ID or password missing in request")
#             return Response(
#                 {
#                     'success': False,
#                     'message': 'Employee ID and password are required'
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         session = SessionLocal()
#         try:
#                 logger.info("Checking for active employee with ID: %s", employee_id)
#                 employee = session.query(Employee).filter_by(
#                     employee_id=employee_id,
#                     is_active=True
#                 ).first()
                
                
#                 if not employee:
#                     logger.warning("Gnvalid credentials or inactive account for employee_id: %s", employee_id)
#                     return Response(
#                         {
#                             'success': False,
#                             'message': 'Invalid credentials or inactive account'
#                         },
#                         status=status.HTTP_401_UNAUTHORIZED
#                     )
                
#                 # Verify password
#                 logger.info("Verifying password for employee_id: %s", employee_id)
#                 if not bcrypt.checkpw(
#                     password.encode('utf-8'), 
#                     employee.password.encode('utf-8')
#                 ):
#                     logger.warning("Invalid password for employee_id: %s", employee_id)
#                     return Response(
#                         {
#                             'success': False,
#                             'message': 'Invalid credentials'
#                         },
#                         status=status.HTTP_401_UNAUTHORIZED
#                     )
                
#                 if twoFactorValue:
#                     logger.info("2FA is enabled for employee_id: %s", employee_id)
#                     otp = generate_otp()
#                     employee.two_fa_enabled=True
#                     print("DONE DONE DONE DONE")
#                     session.commit()

#                     # Store OTP in database
#                     otp_entry = EmployeeOTP(
#                     emp_id=employee.employee_id,
#                     otp=otp,
#                     is_used=False,
#                     is_expired=False
#                     )
#                     session.add(otp_entry)
#                     session.commit()

#                     contact= session.query(ContactDetails).filter_by(employee_id=employee.employee_id).first()
#                     email=contact.email
#                     send_otp_email.delay(email, otp)
#                     # send_mail(
                    
#                     logger.info("OTP sent to registered email: %s", email)
#                     return Response({
#                             'success': True,
#                             'message': 'OTP sent to registered email',
#                             'enable_2fa': True,
#                             '2FactorAuthentication': 'Congrats! 2FA enabled',
#                             'data': {
#                                 'employee_id': employee.employee_id,
#                                 'emp_email': email
#                             }
#                         })
                    
#                 else:
#                     # Generate token
#                     employee.two_fa_enabled= False
#                     session.commit()
#                     token = generate_token(employee.employee_id, employee.role)
                    
#                     #websockets integration
                   

                    
#                     print("2FA Disabled")
#                     return Response({
#                         'success': True,
#                         'message': 'Login successful',
#                         'enable_2fa': False,
#                         'data': {
#                             'token': token,
#                             'employee_id': employee.employee_id,
#                             'role': employee.role
#                         }
#                     })
#         except Exception as e:
#             return Response(
#                 {"success": False, "message": str(e)},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
#         finally:
#             session.close()




#this is the second login view given by claude ai above one is my default
class LoginView(APIView):
    """Handle employee login and token generation."""
    
    def post(self, request):
        try:
            employee_id = request.data.get('employee_id')
            password = request.data.get('password')
            two_factor_value = request.data.get('enable_2fa', False)
            
            logger.debug("Login attempt started for employee_id: %s", employee_id)
            
            # Input validation
            if not all([employee_id, password]):
                logger.warning("Employee ID or password missing in request")
                return Response(
                    {'success': False, 'message': 'Employee ID and password are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            with SessionLocal() as session:
                employee = session.query(Employee).filter_by(
                    employee_id=employee_id,
                    is_active=True
                ).first()
                
                if not employee:
                    logger.warning("Invalid credentials or inactive account for employee_id: %s", employee_id)
                    return Response(
                        {'success': False, 'message': 'Invalid credentials or inactive account'},
                        status=status.HTTP_401_UNAUTHORIZED
                    )
                
                # Verify password using constant-time comparison
                try:
                    password_valid = bcrypt.checkpw(
                        password.encode('utf-8'), 
                        employee.password.encode('utf-8')
                    )
                except ValueError as e:
                    logger.error("Password verification error: %s", str(e))
                    return Response(
                        {'success': False, 'message': 'Authentication error'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                
                if not password_valid:
                    logger.warning("Invalid password for employee_id: %s", employee_id)
                    return Response(
                        {'success': False, 'message': 'Invalid credentials'},
                        status=status.HTTP_401_UNAUTHORIZED
                    )
                
                if two_factor_value:
                    return self._handle_2fa_flow(session, employee)
                else:
                    return self._handle_regular_login(session, employee)
                    
        except Exception as e:
            logger.error("Unexpected error during login: %s", str(e))
            return Response(
                {"success": False, "message": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _handle_2fa_flow(self, session, employee):
        """Handle 2FA login flow."""
        try:
            otp = generate_otp()
            employee.two_fa_enabled = True
            session.commit()

            otp_entry = EmployeeOTP(
                emp_id=employee.employee_id,
                otp=otp,
                is_used=False,
                is_expired=False
            )

            print("Gautam is Debugging")
            session.add(otp_entry)
            session.commit()

            contact = session.query(ContactDetails).filter_by(
                employee_id=employee.employee_id
            ).first()
            
            if not contact or not contact.email:
                raise ValueError("Contact details not found")
                
            send_otp_email.delay(contact.email, otp)
            logger.info("OTP sent to registered email: %s", contact.email)
            
            return Response({
                'success': True,
                'message': 'OTP sent to registered email',
                'enable_2fa': True,
                '2FactorAuthentication': 'Congrats! 2FA enabled',
                'data': {
                    'employee_id': employee.employee_id,
                    'emp_email': contact.email
                }
            })
        except Exception as e:
            logger.error("Error in 2FA flow: %s", str(e))
            session.rollback()
            raise

    def _handle_regular_login(self, session, employee):
        """Handle regular login flow."""
        try:
            employee.two_fa_enabled = False
            session.commit()
            
            token = generate_token(employee.employee_id, employee.role)
            
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
            logger.error("Error in regular login: %s", str(e))
            session.rollback()
            raise


#     'Hurray! you have enabled 2FA.Your Login OTP',
                    #     f'Your OTP for login is {otp}. It is valid for just one use.',
                    #     'noreply@company.com',
                    #     [email],  # Assuming `email` field exists in Employee model
                    #     fail_silently=False,
                    #     )






# class VerifyOTPView(APIView):
#     """Verify OTP and provide authentication token."""

#     def post(self, request):
        

#         employee_id = request.data.get('employee_id')
#         otp = request.data.get('otp')

#         if not employee_id or not otp:
#             return Response(
#                 {
#                     'success': False,
#                     'message': 'Employee ID and OTP are required'
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         session = SessionLocal()
#         try:
#             # Fetch employee
#             employee = session.query(Employee).filter_by(
#                 employee_id=employee_id,
#                 is_active=True
#             ).first()

#             if not employee:
#                 return Response(
#                     {
#                         'success': False,
#                         'message': 'Invalid Employee ID or inactive account'
#                     },
#                     status=status.HTTP_401_UNAUTHORIZED
#                 )

#             # Fetch latest OTP for the employee
#             otp_entry = session.query(EmployeeOTP).filter_by(
#                 emp_id=employee_id,
#                 otp=otp,
#                 is_used=False,
#                 is_expired=False
#             ).order_by(EmployeeOTP.created_on.desc()).first()
            
            
#             if not otp_entry:
#                 return Response(
#                     {
#                         'success': False,
#                         'message': 'Invalid or expired OTP'
#                     },
#                     status=status.HTTP_401_UNAUTHORIZED
#                 )

#             #Check if OTP is expired (valid for 10 minutes)
#             otp_expiry_time = otp_entry.created_on + timedelta(minutes=1)
#             if datetime.now(timezone.utc) > otp_expiry_time.replace(tzinfo=timezone.utc):
#                 otp_entry.is_expired = True
#                 session.commit()
#                 return Response(
#                     {
#                         'success': False,
#                         'message': 'OTP has expired. Please request a new one.'
#                     },
#                     status=status.HTTP_401_UNAUTHORIZED
#                 )


#             # otp_created_time = otp_entry.created_on
            

#             # Mark OTP as used
#             otp_entry.is_used = True
#             session.commit()

#             # Generate token
#             token = generate_token(employee.employee_id, employee.role)
           

#             return Response({
#                 'success': True,
#                 'message': 'OTP verified successfully',
#                 'data': {
#                     'token': token,
#                     'employee_id': employee.employee_id,
#                     'role': employee.role
#                 }
#             })
#         except Exception as e:
#             session.rollback()
#             return Response(
#                 {"success": False, "message": str(e)},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
#         finally:
#             session.close()


class VerifyOTPView(APIView):
    """Verify OTP and provide authentication token."""

    def post(self, request):
        employee_id = request.data.get('employee_id')
        otp = request.data.get('otp')

        if not employee_id or not otp:
            return Response(
                {'success': False, 'message': 'Employee ID and OTP are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        session = None
        try:
            session = SessionLocal()

            # Fetch employee
            employee = session.query(Employee).filter_by(
                employee_id=employee_id, is_active=True
            ).first()

            if not employee:
                return Response(
                    {'success': False, 'message': 'Invalid Employee ID or inactive account'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Fetch latest OTP for the employee
            otp_entry = session.query(EmployeeOTP).filter_by(
                emp_id=employee_id, otp=otp, is_used=False, is_expired=False
            )

            if otp_entry is not None:  # Ensure the query result is not None
                otp_entry = otp_entry.order_by(EmployeeOTP.created_on.desc()).first()
            else:
                 otp_entry = None

            if not otp_entry:
                logger.debug("Querying EmployeeOTP table for OTP verification")

                return Response(
                    {'success': False, 'message': 'Invalid or expired OTP'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Ensure `created_on` is valid before checking expiry
            if not otp_entry.created_on:
                return Response(
                    {'success': False, 'message': 'OTP timestamp error. Please request a new one.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Check if OTP is expired
            otp_expiry_time = otp_entry.created_on + timedelta(minutes=10)
            if datetime.now(timezone.utc) > otp_expiry_time.replace(tzinfo=timezone.utc):
                otp_entry.is_expired = True
                session.commit()
                return Response(
                    {'success': False, 'message': 'OTP has expired. Please request a new one.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Mark OTP as used
            otp_entry.is_used = True
            session.commit()

            # Generate token safely
            try:
                token = generate_token(employee.employee_id, employee.role)
            except Exception as e:
                session.rollback()
                logger.error(f"Token generation error: {str(e)}", exc_info=True)  # Log error
                return Response(
                    {'success': False, 'message': 'Token generation failed. Try again later.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            return Response({
                'success': True,
                'message': 'OTP verified successfully',
                'data': {
                    'token': token,
                    'employee_id': employee.employee_id,
                    'role': employee.role
                }
            })

        except IntegrityError:
            if session:
                session.rollback()
            return Response(
                {'success': False, 'message': 'Database integrity error. Please try again.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except SQLAlchemyError:
            if session:
                session.rollback()
            return Response(
                {'success': False, 'message': 'Database error. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except Exception as e:
            if session:
                session.rollback()
            logger.error(f"Error in verifyOTP: {str(e)}", exc_info=True)    
            return Response(
                {'success': False, 'message': 'An unexpected error occurred. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        finally:
            if session:
                session.close()


















# Manager: Kartavya Login Credentials:

# "employee_id": "EMP202502080509232383",
# "password": "d(:TD*wU2Qig",


#  channel_layer = get_channel_layer()
#                     async_to_sync(channel_layer.group_send)(
#                     "login_updates",
#                     {
#                         "type": "send_login_update",
#                         "message": {
#                             "employee_id": employee.employee_id,
#                             "message": f"{employee.employee_name} has logged in!"
#                         }
#                     }
#                 )





#if otp_created_time.tzinfo is None:
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