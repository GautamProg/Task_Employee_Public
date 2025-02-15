# employee_management/models/models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, func, create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime


DATABASE_URL = "mysql+pymysql://root:gautam_prog@localhost/employee_db"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employees'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(String(50), unique=True, nullable=False)
    employee_name = Column(String(100), nullable=False)
    department = Column(String(50), nullable=False)
    manager_id = Column(String(50), ForeignKey('employees.employee_id'), nullable=True)
    salary = Column(Float, nullable=False)
    joining_date = Column(DateTime, default=func.now())
    role = Column(String(20), nullable=False)  # 'EMPLOYEE', 'MANAGER', 'ADMIN'
    is_active = Column(Boolean, default=True)
    password = Column(String(255), nullable=False)
    two_fa_enabled = Column(Boolean, default=False)
    
    manager = relationship("Employee", remote_side=[employee_id])
    contact_details = relationship("ContactDetails", back_populates="employee", uselist=False)
    address_details = relationship("AddressDetails", back_populates="employee", uselist=False)

class ContactDetails(Base):
    __tablename__ = 'contact_details'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(String(50), ForeignKey('employees.employee_id'), unique=True)
    phone = Column(String(20))
    email = Column(String(100))
    
    employee = relationship("Employee", back_populates="contact_details")

class AddressDetails(Base):
    __tablename__ = 'address_details'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(String(50), ForeignKey('employees.employee_id'), unique=True)
    city = Column(String(50))
    state = Column(String(50))
    country = Column(String(50))
    location = Column(String(255))
    landmark = Column(String(255))
    
    employee = relationship("Employee", back_populates="address_details")



class EmployeeOTP(Base):
    __tablename__ = "employee_otp"

    id = Column(Integer, primary_key=True, autoincrement=True)
    emp_id = Column(String(50), nullable=False)  # Employee ID
    otp = Column(String(6), nullable=False)  # 6-digit OTP
    is_used = Column(Boolean, default=False)  # If OTP is used
    is_expired = Column(Boolean, default=False)  # If OTP is expired
    created_on = Column(DateTime, default=func.now())  # OTP generation time
    updated_on = Column(DateTime, default=func.now(), onupdate=func.now())  # Last updated time


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)



Base.metadata.create_all(engine)

# hello