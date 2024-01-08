from pydantic import BaseModel, StringConstraints
from typing_extensions import Annotated


class Admin(BaseModel):
    first_name: Annotated[str, StringConstraints(max_length=30)]
    last_name: Annotated[str, StringConstraints(max_length=30)]
    username: Annotated[str, StringConstraints(max_length=30)]
    email: Annotated[str, StringConstraints(max_length=100)]  
    password: Annotated[str, StringConstraints(max_length=72)] 