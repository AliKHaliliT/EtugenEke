from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, String 
from datetime import datetime


Base = declarative_base()

class Plans(Base):
    __tablename__ = "Plans"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_created = Column(DateTime, default=datetime.utcnow)
    plan = Column(String(50), nullable=False, unique=True)
    credit = Column(String(50), nullable=False)
    price = Column(String(50), nullable=False)
    services = Column(String(50), nullable=False) # Must be defined as a comma separated string
    description = Column(String(50), nullable=True, default="No Description.")
