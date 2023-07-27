import contextlib
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE, DB_DATABASE_2

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
SQLALCHEMY_DATABASE_URL_2 = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE_2}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
engine2 = create_engine(SQLALCHEMY_DATABASE_URL_2)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocal2 = sessionmaker(autocommit=False, autoflush=False, bind=engine2)

Base = declarative_base()

@contextlib.contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
     
def get_db2():
    db = SessionLocal2()
    try:
        yield db
    finally:
        db.close()