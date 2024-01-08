from sqlalchemy.ext.declarative import declarative_base
from fastapi_storages import FileSystemStorage
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from fastapi_storages.integrations.sqlalchemy import FileType


Base = declarative_base()
storage = FileSystemStorage(path="../uploads")

class LamenessDetectionVideos(Base):
    __tablename__ = "LamenessDetectionVideo"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    date_uploaded = Column(DateTime, default=datetime.utcnow)
    file = Column(FileType(storage=storage), nullable=False)
    lameness_status = Column(String(64), nullable=False)