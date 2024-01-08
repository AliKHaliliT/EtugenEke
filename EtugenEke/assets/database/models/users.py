from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, String, Boolean 
from datetime import datetime


Base = declarative_base()

class Users(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_created = Column(DateTime, default=datetime.utcnow)
    role = Column(String(50), nullable=False, default="user")
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(120), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    plan = Column(String(50), nullable=False)
    credit = Column(Integer, nullable=False)
    recharged = Column(Boolean, nullable=False, default=False)
    token = Column(String(128), nullable=False, default='')
