from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:missdezi06@localhost/fastapi_project"

engine = create_engine(DATABASE_URL)

Base = declarative_base()
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)