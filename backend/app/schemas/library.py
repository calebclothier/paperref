from pydantic import BaseModel


class Paper(BaseModel):
    doi: str
    title: str