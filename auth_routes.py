from fastapi import APIRouter, status
from database import SessionLocal, engine
from schemas_auth import SignUp
from models import Users
from werkzeug.security import generate_password_hash, check_password_hash

auth_router = APIRouter(
    prefix="/auth"
)


@auth_router.post("/signup", status_code=201)
async def signup(user: SignUp):
    session = SessionLocal()

    db_email = session.query(Users).filter(Users.email == user.email).first()
    if db_email is not None:
        return {"message": "Email already exists", "status_code": status.HTTP_400_BAD_REQUEST}
    db_username = session.query(Users).filter(Users.username == user.username).first()
    if db_username is not None:
        return {"message": "Username already exists", "status_code": status.HTTP_400_BAD_REQUEST}
    new_user = Users(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff
    )
    session.add(new_user)
    session.commit()
    user_data = {
        'username': user.username,
        'email': user.email,
        'is_active': user.is_active,
        'is_staff': user.is_staff
    }

    return {"message": "User created successfully",
            "new_user": user_data,
            'status': status.HTTP_201_CREATED
            }

