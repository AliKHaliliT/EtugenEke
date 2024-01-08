from sqlalchemy.ext.declarative import declarative_base
from fastapi_storages import FileSystemStorage
from sqlalchemy import Column, Integer, DateTime, String
from datetime import datetime
from fastapi_storages.integrations.sqlalchemy import FileType


Base = declarative_base()
storage = FileSystemStorage(path="../services")

class Services(Base):
    __tablename__ = "Services"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_added = Column(DateTime, default=datetime.utcnow)
    service_name = Column(String)
    service_description = Column(String)
    service_image = Column(FileType(storage=storage), nullable=False)
