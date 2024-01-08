from pydantic import BaseModel, StringConstraints
from typing_extensions import Annotated



class Auth(BaseModel):
    username_or_email: Annotated[str, StringConstraints(max_length=100)]  
    password: Annotated[str, StringConstraints(max_length=72)]