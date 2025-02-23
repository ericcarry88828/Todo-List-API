from pydantic import BaseModel, Field


class TodoCreateUpdate(BaseModel):
    title: str
    description: str = Field(max_length=255)
