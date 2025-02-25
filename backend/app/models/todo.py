from sqlmodel import SQLModel, Field


class Todo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str
    user_id: int | None = Field(default=None, foreign_key="user.id")
