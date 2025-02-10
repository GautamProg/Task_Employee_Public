# authentication/utils.py
import jwt
import random
import string
import bcrypt
from datetime import datetime, timedelta, timezone
from django.conf import settings
from employee_management.models.models import SessionLocal, Employee
from django.core.cache import cache

def generate_token(employee_id, role):
    """Generate JWT token for authenticated users."""
    payload = {
        'employee_id': employee_id,
        'role': role,
        'exp': datetime.now(timezone.utc) + timedelta(days=1)
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

def verify_token(token):
    """Verify and decode JWT token."""
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def generate_password(length=12):
    """Generate a secure random password."""
    characters = string.ascii_letters + string.digits + string.punctuation.replace('"', '').replace('\\', '')
    # return ''.join(random.choice(characters) for _ in range(length))
    plain_password = ''.join(random.choice(characters) for _ in range(length))
    
    # Hash the password
    hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    return (plain_password, hashed_password)

def generate_employee_id(prefix="EMP"):
    """Generate unique employee ID."""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_suffix = ''.join(random.choices(string.digits, k=4))
    return f"{prefix}{timestamp}{random_suffix}"




def generate_otp():
    return str(random.randint(100000, 999999))





def get_employee_from_cache(employee_id):
    cache_key = f'employee_{employee_id}'
    employee = cache.get(cache_key)
    session=SessionLocal()
    if not employee:
        session = SessionLocal()
        employee = session.query(Employee).filter_by(employee_id=employee_id, is_active=True).first()
        session.close()

        if employee:
            cache.set(cache_key, employee, timeout=300)  # Cache for 5 mins

    return employee





def invalidate_employee_cache(employee_id):
    cache.delete(f'employee_{employee_id}')



def cache_otp(employee_id, otp):
    cache.set(f'otp_{employee_id}', otp, timeout=300)  # OTP valid for 5 mins

# Retrieve OTP from cache
def get_cached_otp(employee_id):
    return cache.get(f'otp_{employee_id}')



