from sqlalchemy import Column, Integer, String, Boolean, Enum
from database import Base
from enums.roleenum import UserRole

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Integer, default=UserRole.employee.value, nullable=False)
    is_active = Column(Boolean, default=True)
