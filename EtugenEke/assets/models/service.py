from pydantic import BaseModel, StringConstraints
from typing_extensions import Annotated


class Service(BaseModel):
    service_name: Annotated[str, StringConstraints(max_length=50)]
    service_description: str 