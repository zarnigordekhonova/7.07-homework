from fastapi import APIRouter
from database import SessionLocal
from schemas_auth import SignUp
from models import Users
from werkzeug.security import generate_password_hash, check_password_hash

auth_router = APIRouter(prefix='/auth')


@auth_router.post("/signup")
async def signup(user: SignUp):
    session = SessionLocal()

    db_email = session.query(Users).filter(Users.email == user.email).first()
    if db_email is not None:
        return {"message": "Email already exists"}

    db_username = session.query(Users).filter(Users.username == user.username).first()
    if db_username is not None:
        return {"message": "Username already exists"}

    new_user = Users(
        email=user.email,
        username=user.username,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff
    )
    session.add(new_user)
    session.commit()

    return {"message": "user created successfully",
            "new_user": new_user
            }

