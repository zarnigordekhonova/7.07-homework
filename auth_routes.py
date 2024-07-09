from fastapi import APIRouter, status, HTTPException, Depends
import datetime
from fastapi.encoders import jsonable_encoder
from sqlalchemy import or_
from database import SessionLocal, engine
from schemas_auth import SignUp, LoginModel
from models import Users
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT



auth_router = APIRouter(
    prefix="/auth"
)


@auth_router.get("/")
async def get_auth(Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token entered')
    return {'message': "Hello auth"}


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


@auth_router.post('/login', status_code=200)
async def login(user:LoginModel, Authorize: AuthJWT=Depends()):
    session = SessionLocal()

    db_user = session.quert(Users).filter(
        or_(
            Users.username == user.username_or_email,
            Users.email == user.username_or_email
        )
    ).first()

    if db_user and check_password_hash(db_user.password, user.password):
        access_lifetime = datetime.timedelta(minutes=60)
        refresh_lifetime = datetime.timedelta(days=3)
        access_token = Authorize.create_access_token(subject=db_user.username, expires_time=access_lifetime)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username, expires_time=refresh_lifetime)
        token = {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

        response_data = {
            "message": "Successfully logged in",
            "status": status.HTTP_200_OK,
            "token": token
        }

        return response_data
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username/email or password!")


@auth_router.get("/login/refresh", status_code=200)
async def refresh_token(Authorize: AuthJWT=Depends()):
    session = SessionLocal()

    try:
        access_lifetime = datetime.timedelta(minutes=60)
        Authorize.jwt_refresh_token_required()
        current_user = Authorize.get_jwt_subject()
        db_user = session.query(Users).filter(Users.username == current_user).first()
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")

        new_refresh_token = Authorize.create_refresh_token(subject=db_user.username, expires_time=access_lifetime)
        response_model = {
            'Success' : True,
            "refresh" : new_refresh_token
        }
        return jsonable_encoder(response_model)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


@auth_router.post('/logout')
async def logout(Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
        jti = Authorize.get_raw_jwt()['jti']
        response = {
            "message" : "Successfully logged out"
        }
        return jsonable_encoder(response)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")