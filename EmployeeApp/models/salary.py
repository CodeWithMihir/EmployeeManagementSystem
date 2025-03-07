from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Salary(Base):
    __tablename__ = "salaries"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), unique=True, nullable=False)
    
    base_salary = Column(Float, nullable=False, default=0)
    special_allowance = Column(Float, nullable=False, default=0)
    bonus = Column(Float, nullable=False, default=0)

    # Computed column for total amount not supported in sqlite3 so removing the logic
    #amount = Column(Float, Computed("base_salary + special_allowance + bonus", persisted=True))
    
    #calculating total in python itself
    @property
    def amount(self):
        return self.base_salary + self.special_allowance + self.bonus

    employee = relationship("Employee", back_populates="salary")
    