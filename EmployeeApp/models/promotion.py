from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from database import Base

class Promotion(Base):
    __tablename__ = "promotions"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    promotion_date = Column(DateTime, default=func.now())
    new_position = Column(String, nullable=False)

    #One employee can have many promotions
    employee = relationship("Employee", back_populates="promotions")
