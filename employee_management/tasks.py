from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

@shared_task
def send_otp_email(email, otp):
    """Send OTP email asynchronously using Celery."""
    try:
        send_mail(
            'Hurray! You have enabled 2FA. Your Login OTP',
            f'Your OTP for login is {otp}. It is valid for just one use.',
            'noreply@company.com',
            [email],
            fail_silently=False,
        )
        return f"OTP email sent to {email}"
    except Exception as e:
        return f"Error sending email: {str(e)}"
    






@shared_task
def send_employee_credentials_email(employee_email, employee_name, employee_id, password):
    subject = "Your Employee Login Credentials"
    message = f"""
    Dear {employee_name},

    Welcome to the company! Your login credentials are:

    Employee ID: {employee_id}
    Password: {password}  

    Please log in and change your password after first login.

    Best Regards,
    Company HR
    """

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [employee_email],
        fail_silently=False
    )
    return f"Employee credentials email sent to {employee_email}"
