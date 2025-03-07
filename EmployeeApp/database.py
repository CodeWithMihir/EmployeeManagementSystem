from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = 'sqlite:///./employeesapp.db'

engine = create_engine(DATABASE_URL, connect_args={'check_same_thread':False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#I am using controllers so instead of defining in every controller i defined the method here
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()