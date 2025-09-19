from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "sqlite:///online_magazine_db.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


LocalSession = sessionmaker(bind=engine, autoflush=False, autocommit = False)

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

class BaseModel(DeclarativeBase):
    pass