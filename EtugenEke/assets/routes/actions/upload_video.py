import logging
from fastapi import APIRouter, Form, File
from sqlalchemy.orm import sessionmaker
from assets.database.db.etugeneke_db import engine
from assets.models.upload_video import UploadVideo
from assets.database.models.users import Users
from assets.database.models.lameness_detection_videos import LamenessDetectionVideos
from fastapi.responses import JSONResponse, Response
import os
from datetime import datetime
import random


# Configure logging
logging.basicConfig(level=logging.DEBUG) 

file_handler = logging.FileHandler(r'E:\Ongoing\Python\EtugenEke\logs\upload_video.log')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logging.getLogger('').addHandler(file_handler)


router = APIRouter()
Session = sessionmaker(bind=engine)

@router.post("/actions/upload_video/")
async def upload_video(username_or_email: str = Form(...), 
                       health_status: str = Form(...),
                       file = File(...)) -> JSONResponse:

    """
    
    This endpoint sends the video and saves it to the database.


    Parameters
    ----------
    username_or_email: str
        The username or email of the user.

    file: File
        The video file.

    health_status: str
        The health status of the animal in the video.


    Returns
    -------
    response: JSONResponse
        A JSON response containing the status of the data submission request.

    """

    logging.info(f"Received: {username_or_email}, {file}, {health_status} as payload")

    try:

        # Validate the parameters
        upload_video = UploadVideo(username_or_email=username_or_email, file=file, health_status=health_status)
        

        with Session() as session:

            # Check if the user exists
            user = session.query(Users).filter(Users.username == upload_video.username_or_email).first()

            if not user:
                logging.error(f"User {upload_video.username_or_email} does not exist")
                return JSONResponse(content={"message": "User does not exist."}, status_code=404)

            # Dummy inference
            date_uploaded = datetime.utcnow()

            upload_video.file.filename = os.path.splitext(file.filename)[0] + f"{date_uploaded}_{random.random()}.mp4"

            # Save the video and inference result to the database
            video_record = LamenessDetectionVideos(
                username=upload_video.username_or_email,
                date_uploaded=date_uploaded,
                file=upload_video.file,
                lameness_status=upload_video.health_status
            )
            session.add(video_record)

            session.commit()

            
            logging.info(f"User {upload_video.username_or_email} uploaded video {upload_video.file.filename} successfully")
            return JSONResponse(content={"message": "Video uploaded successfully."}, status_code=200)
    except Exception as e:
        logging.error(f"Error in uploading video: {e}", exc_info=True)
        return Response(status_code=500)