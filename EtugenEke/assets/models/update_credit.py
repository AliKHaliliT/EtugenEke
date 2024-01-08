from pydantic import BaseModel


class UpdateCredit(BaseModel):
    credit: int