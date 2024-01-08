from pydantic import BaseModel, StringConstraints
from typing_extensions import Annotated


class ResetPassword(BaseModel):
    token: Annotated[str, StringConstraints(max_length=100)]  
    new_password: Annotated[str, StringConstraints(max_length=72)]