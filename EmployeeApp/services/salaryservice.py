from sqlalchemy.orm import Session
from models import Salary
import schemas
from fastapi import HTTPException
from http import HTTPStatus

def create_salary(db: Session, salary_data: schemas.SalaryCreate):
    existing_salary = db.query(Salary).filter(Salary.employee_id == salary_data.employee_id).first()
    if existing_salary:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Employee already has a salary. Please use update salary option.")

    new_salary = Salary(
        employee_id=salary_data.employee_id,
        base_salary=salary_data.base_salary,
        special_allowance=salary_data.special_allowance,
        bonus=salary_data.bonus
    )
    db.add(new_salary)
    db.commit()
    db.refresh(new_salary)
    return new_salary

def get_salary_by_employee_id(db: Session, employee_id: int):
    salary = db.query(Salary).filter(Salary.employee_id == employee_id).first()
    if not salary:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Salary not found for this employee")

    return schemas.SalaryResponse(
        id=salary.id,
        employee=schemas.EmployeeBase(
            id=salary.employee.id,
            name=salary.employee.name,
            age=salary.employee.age,
            position=salary.employee.position,
            department_id=salary.employee.department_id,
        ),
        base_salary=salary.base_salary,
        special_allowance=salary.special_allowance,
        bonus=salary.bonus,
        amount=salary.amount  # Computed dynamically
    )

def update_salary(db: Session, employee_id: int, increment: float):
    salary = db.query(Salary).filter(Salary.employee_id == employee_id).first()
    if not salary:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Salary record not found")
    
    salary.amount += increment
    salary.last_increment = increment
    db.commit()
    db.refresh(salary)
    return salary

def delete_salary(db: Session, employee_id: int):
    salary = db.query(Salary).filter(Salary.employee_id == employee_id).first()
    if not salary:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Salary record not found")
    db.delete(salary)
    db.commit()
    return {"message": "Salary record deleted successfully"}
