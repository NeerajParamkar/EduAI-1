from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class SignupUser(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    confirm_password: str = Field(min_length=6)

class LoginUser(BaseModel):
    email: EmailStr
    password: str
