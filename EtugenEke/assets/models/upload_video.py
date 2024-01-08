from pydantic import BaseModel, StringConstraints
from typing_extensions import Annotated
from fastapi import UploadFile


class UploadVideo(BaseModel):
    username_or_email: Annotated[str, StringConstraints(max_length=64)]  
    file: UploadFile
    health_status: Annotated[str, StringConstraints(max_length=64)]