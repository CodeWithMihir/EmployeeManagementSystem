from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Department(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)

    #Department can have multiple employees, meaning it is one-to-many relationship.
    #Department can have multiple employees, but each Employee belongs to only one Department
    employees = relationship("Employee", back_populates="department")