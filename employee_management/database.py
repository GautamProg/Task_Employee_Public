# employee_management/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from django.conf import settings

# Create engine instance
engine = create_engine("mysql+pymysql://root:gautam_prog@localhost/employee_db")

# Create session factory
SessionFactory = sessionmaker(bind=engine)

# Create scoped session
Session = scoped_session(SessionFactory)

def get_session():
    """Get a database session."""
    session = Session()
    try:
        return session
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.remove()