from pydantic import BaseModel
from typing import Literal

class RegisterSchema(BaseModel):
    name: str
    email: str
    password: str
    role: Literal["admin", "employee"] = "employee"

class LoginSchema(BaseModel):
    email: str
    password: str