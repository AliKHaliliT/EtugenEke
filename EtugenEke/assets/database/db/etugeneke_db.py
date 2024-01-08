from sqlalchemy import create_engine
from assets.database.models.admins import Base as AdminsBase
from assets.database.models.users import Base as UsersBase
from assets.database.models.lameness_detection_data import Base as LamenessDetectionBase
from assets.database.models.lameness_detection_videos import Base as LamenessDetectionVideosBase
from assets.database.models.services import Base as ServicesBase
from assets.database.models.plans import Base as PlansBase


# Create the SQLite engine
engine = create_engine("sqlite:///EtugenEke.db", connect_args={"check_same_thread": False})


# Create tables in the database
AdminsBase.metadata.create_all(engine)
UsersBase.metadata.create_all(engine)
LamenessDetectionBase.metadata.create_all(engine)
LamenessDetectionVideosBase.metadata.create_all(engine)
ServicesBase.metadata.create_all(engine)
PlansBase.metadata.create_all(engine)
