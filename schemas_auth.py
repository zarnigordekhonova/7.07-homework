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
        orm_mode = True
        schema_extra = {
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
    authjwt_algorithm: str = "HS256"


class OrdersModel(BaseModel):
    id: Optional[int]
    user_id: int
    product_id: int
    status: Optional[str]
    quantity: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example":{
                'quantity': 1
            }
        }


class OrderStatus(BaseModel):
    order_status: Optional[str] = "PENDING"

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                'order_status': 'PENDING'
            }
        }

class ProductsModel(BaseModel):
    id: Optional[int]
    name: str
    description: Optional[str]
    price: float

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                'name': 'Example product',
                'price': 25.3
            }
        }


class ProductUpdateModel(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None

    class Config:
        orm_mode = True


class OrdersUpdateModel(BaseModel):
    product_id: Optional[int] = None
    status: Optional[str] = None
    quantity: Optional[int] = None


    class Config:
        orm_mode = True




