from pydantic import BaseModel, StringConstraints
from typing_extensions import Annotated


class ForgotPassword(BaseModel):
    username_or_email: Annotated[str, StringConstraints(max_length=100)] 