from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=6, max_length=22)


class UserLogin(BaseModel):
    email: EmailStr
    password: str
