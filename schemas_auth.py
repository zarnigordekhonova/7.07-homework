from pydantic import BaseModel, Field
from typing import Optional



class SignUp(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    password: str
    is_staff: bool
    is_active: bool

    class Config:
        from_attributes = True
        json_schema_extra = {
            'example': {
                "username": 'john_doe03',
                "email": 'john_doe@example.com',
                "password": 'secret_key',
                "is_staff": False,
                "is_active": True
            }
        }


class LoginModel(BaseModel):
    username_or_email: str
    password: str


class Settings(BaseModel):
    authjwt_secret_key: str = "80b6fd5b764042a7e392d48df7b46422276cfbe2189d9b933397251dd38e8e70"