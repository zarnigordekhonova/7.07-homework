from pydantic import BaseModel, EmailStr
from typing import Optional


class SignUp(BaseModel):
    id: Optional[int] = None
    username: str
    email: EmailStr
    password: str
    is_staff: bool = False
    is_active: bool = True

    class Config:
        json_schema_extra = {
            'example': {
                "username": 'john_doe03',
                "email": 'john_doe@example.com',
                "password": 'secret_key',
                "is_staff": False,
                "is_active": True
            }
        }
