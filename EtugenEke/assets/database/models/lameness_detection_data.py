from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()

class LamenessDetectionData(Base):
    __tablename__ = "LamenessDetection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    date = Column(String(50), nullable=False)
    healthy = Column(Integer, nullable=False)
    lame = Column(Integer, nullable=False)
    fir = Column(Integer, nullable=False)
    uncertain = Column(Integer, nullable=False)