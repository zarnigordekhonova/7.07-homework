from database import engine, Base
from models import Users, Orders, Products

Base.metadata.create_all(bind=engine)
