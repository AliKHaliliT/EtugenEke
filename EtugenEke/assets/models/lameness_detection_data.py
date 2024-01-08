from pydantic import BaseModel, StringConstraints
from typing_extensions import Annotated


class LamenessDetectionData(BaseModel):
    username: Annotated[str, StringConstraints(max_length=30)]
    date: str
    healthy: int
    lame: int
    fir: int
    uncertain: int