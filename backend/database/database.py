from sqlmodel import create_engine, Session
from sqlalchemy import MetaData
from models.user import User
from models.task import Task
from config import DATABASE_URL


# Create database engine
engine = create_engine(DATABASE_URL, echo=False)


def get_session():
    """Yield a database session"""
    with Session(engine) as session:
        yield session


def create_tables():
    """Create all tables in the database"""
    from sqlmodel import SQLModel
    
    # Import all models to ensure they're registered with SQLModel
    # This is necessary for create_all to work properly
    
    SQLModel.metadata.create_all(engine)