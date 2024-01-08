from pydantic import BaseModel, StringConstraints
from typing_extensions import Annotated
from fastapi import UploadFile


class Inference(BaseModel):
    service_type: Annotated[str, StringConstraints(max_length=64)]  
    file: UploadFile