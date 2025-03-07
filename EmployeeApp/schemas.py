from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional, List

from enums.roleenum import UserRole

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: int = Field(..., description="Role must be 1 (admin), 2 (manager), or 3 (employee)", ge=1, le=3)

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str

    @classmethod
    def from_orm(cls, user):
        """Convert integer role to string based on UserRole Enum"""
        return cls(
            id=user.id,
            username=user.username,
            email=user.email,
            role=UserRole(user.role).name  # Convert int -> string (e.g., 1 -> "admin")
        )

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class DepartmentBase(BaseModel):
    name: str = Field(min_length=3, max_length=20)
    description: Optional[str] = None

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentResponse(DepartmentBase):
    id: int

    class Config:
        from_attributes = True

class EmployeeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=18, le=100) 
    position: str
    department_id: Optional[int] = None
    
    class Config:
        from_attributes = True

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeResponse(EmployeeBase):
    id: int

    class Config:
        from_attributes = True

class PromotionBase(BaseModel):
    employee_id: int
    new_position: str

class PromotionCreate(PromotionBase):
    pass

class PromotionResponse(PromotionBase):
    id: int
    promotion_date: datetime

    class Config:
        from_attributes = True

class SalaryBase(BaseModel):
    employee_id: int
    amount: float = Field(gt=-1)
    last_increment: float = 0

class SalaryCreate(BaseModel):
    employee_id: int
    base_salary: float
    special_allowance: float
    bonus: float

class SalaryResponse(BaseModel):
    id: int
    employee: EmployeeBase  # Include employee details
    base_salary: float
    special_allowance: float
    bonus: float
    amount: float  # Total salary

    class Config:
        from_attributes = True
