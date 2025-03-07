from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    position = Column(String, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))

    #department can have multiple employees, meaning it is one-to-many relationship.
    department = relationship("Department", back_populates="employees")
    
    #uselist=False ensures that an Employee has only one associated Salary record
    #This means there is a one-to-one relationship between Employee and Salary.
    salary = relationship("Salary", uselist=False, back_populates="employee")
    
    #one Employee can have multiple Promotion records
    #Each Promotion entry is linked to one Employee, but an Employee can have many promotions
    promotions = relationship("Promotion", back_populates="employee")
