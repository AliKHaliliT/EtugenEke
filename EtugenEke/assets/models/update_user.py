from pydantic import BaseModel, StringConstraints
from typing_extensions import Annotated


class UpdateUser(BaseModel):
    first_name: Annotated[str, StringConstraints(max_length=50)] 
    last_name: Annotated[str, StringConstraints(max_length=50)]
    username: Annotated[str, StringConstraints(max_length=30)]
    email: Annotated[str, StringConstraints(max_length=100)]
    password: Annotated[str, StringConstraints(max_length=72)]