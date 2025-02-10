from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from sqlalchemy.orm import Session
from django.core.mail import send_mail
from django.conf import settings
from ..models.models import Employee, ContactDetails, AddressDetails, SessionLocal
from ..serializers.serializers import EmployeeCreateSerializer, EmployeeResponseSerializer
from authentication.permissions import IsEmployee, IsManager, IsAdmin
from authentication.utils import generate_password, generate_employee_id
from datetime import datetime
from employee_management.tasks import send_employee_credentials_email
from rest_framework.permissions import IsAuthenticated




class EmployeeCreateView(APIView):
   # permission_classes = [IsManager | IsAdmin]
    
    def post(self, request):
        serializer = EmployeeCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"success": False, "errors": serializer.errors}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        session=SessionLocal()
        try:
            data = serializer.validated_data
            personal_details = data['personal_details']
            
            # Generate employee_id and password
            employee_id = generate_employee_id()
            password = generate_password()
            
            # Create employee
            employee = Employee(
                employee_id=employee_id,
                employee_name=personal_details['employee_name'],
                department=personal_details['department'],
                manager_id=personal_details['manager'],
                salary=personal_details['salary'],
                joining_date=datetime.now(),
                role='EMPLOYEE',
                password=password[1]
            )
            session.add(employee)
            
            # Create contact details
            contact = ContactDetails(
                employee_id=employee_id,
                **data['contact_details']
            )
            session.add(contact)
            
            # Create address details
            address = AddressDetails(
                employee_id=employee_id,
                **data['address_details']
            )
            session.add(address)
            
            session.commit()
            
            # Get manager details for response
            manager = session.query(Employee).filter_by(
                employee_id=personal_details['manager']
            ).first()



            employee_email = data['contact_details']['email']
            subject = "Your Employee Login Credentials"
            message = f"""
            Dear {personal_details['employee_name']},

            Welcome to the company! Your login credentials are:

            Employee ID: {employee_id}
            Password: {password[0]}  

            Please log in and change your password after first login.

            Best Regards,
            Company HR
            """


            # send_mail(
            #     subject,
            #     message,
            #     settings.DEFAULT_FROM_EMAIL,
            #     [employee_email],
            #     fail_silently=False
            # )
            send_employee_credentials_email.delay(employee_email, personal_details['employee_name'], employee_id, password[0])
            response_data = {
                "success": True,
                "status_code": status.HTTP_200_OK,
                "message": "Employee Added successfully",
                "data": {
                    "employee_details": {
                        "employee_id": employee_id,
                        "password": password[0],
                        "employee_name": personal_details['employee_name'],
                        "department": personal_details['department'],
                        "manager": {
                            "manager_id": manager.employee_id,
                            "manager_name": manager.employee_name
                        }
                    }
                }
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            session.rollback()
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        finally:
            session.close()

class EmployeeDetailView(APIView):
    permission_classes = [IsAdmin | IsEmployee | IsManager]
    
    def get(self, request, employee_id):
        session = SessionLocal()
        try:
            print(f"Querying employee with ID: {employee_id}")
            employee = session.query(Employee).filter_by(
                employee_id=employee_id
            ).first()
            
            if not employee:
                return Response(
                    {"success": False, "message": "Employee not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            print(f"Request user employee_id: {request.user.employee_id}")
            print(f"Employee ID from URL: {employee_id}")
            # Check permissions
            if request.user.role == 'EMPLOYEE' and request.user.employee_id != employee_id:
                return Response(
                    {"success": False, "message": "Permission denied"},
                    status=status.HTTP_403_FORBIDDEN
                )
                
            # Return employee details
            return Response({
                "success": True,
                "data": {
                    "employee_details": {
                        "employee_id": employee.employee_id,
                        "employee_name": employee.employee_name,
                        "department": employee.department,
                        "manager": {
                            "manager_id": employee.manager.employee_id if employee.manager else None,
                            "manager_name": employee.manager.employee_name if employee.manager else None
                        }
                    }
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









def login_view(request):
    return render(request, 'login.html')


def verify_otp_view(request):
    return render(request, 'verify_otp.html')

def dashboard_view(request):
    return render(request, 'dashboard.html')
