from sqlalchemy.orm import Session
from models.employee import Employee
import schemas
from http import HTTPStatus
from fastapi import HTTPException

def create_employee(db: Session, employee_data: schemas.EmployeeCreate) -> Employee:
    new_employee = Employee(**employee_data.model_dump())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

def get_all_employees(db: Session):
    return db.query(Employee).all()

def get_employee_by_id(db: Session, employee_id: int) -> Employee:
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if employee is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Employee not found.")
    return employee

def update_employee(db: Session, employee_id: int, employee_data: schemas.EmployeeCreate):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if employee is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Employee not found.")

    # Updating fields
    employee.name = employee_data.name
    employee.age = employee_data.age
    employee.position = employee_data.position
    employee.department_id = employee_data.department_id

    db.add(employee)
    db.commit()

def delete_employee(db: Session, employee_id: int):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if employee is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Employee not found.")

    db.delete(employee)
    db.commit()
