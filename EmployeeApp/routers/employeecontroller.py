from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from database import get_db
import schemas
from routers.auth import get_current_user, require_admin, require_manager
from typing import Annotated, List
from services import employeeservice 
from http import HTTPStatus

router = APIRouter(prefix="/employees", tags=["Employee Management"])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.post("/createemployee", response_model=schemas.EmployeeResponse, status_code=HTTPStatus.CREATED)
def create_employee(
    db: db_dependency,
    employee: schemas.EmployeeCreate,
    user: dict = Depends(require_admin)
):
    """
    **Create a new employee**  
    - **Requires Admin role**  
    - **Request Body:** Employee details (`EmployeeCreate` schema)  
    - **Response:** Created employee (`EmployeeResponse` schema)  
    - **Status Code:** 201 Created  
    """
    return employeeservice.create_employee(db, employee)


@router.get("", response_model=List[schemas.EmployeeResponse])
def get_all_employees(user: user_dependency, db: db_dependency):
    """
    **Retrieve all employees**  
    - **Requires Authentication**  
    - **Response:** List of employees (`EmployeeResponse` schema)  
    - **Status Code:** 200 OK  
    """
    return employeeservice.get_all_employees(db)


@router.get("/{employee_id}", response_model=schemas.EmployeeResponse)
def get_employee_by_id(
    user: user_dependency, 
    db: db_dependency, 
    employee_id: int = Path(gt=0)
):
    """
    **Retrieve an employee by ID**  
    - **Requires Authentication**  
    - **Path Parameter:** `employee_id` (integer, must be greater than 0)  
    - **Response:** Employee details (`EmployeeResponse` schema)  
    - **Status Code:** 200 OK  
    - **Errors:** 404 Not Found if employee does not exist  
    """
    return employeeservice.get_employee_by_id(db, employee_id)


@router.put("/{employee_id}", status_code=HTTPStatus.NO_CONTENT)
def update_employee(
    db: db_dependency, 
    employee_update: schemas.EmployeeCreate, 
    employee_id: int = Path(gt=0),
    user: dict = Depends(require_manager)
):
    """
    **Update an existing employee**  
    - **Requires Manager role**  
    - **Path Parameter:** `employee_id` (integer, must be greater than 0)  
    - **Request Body:** Updated employee details (`EmployeeCreate` schema)  
    - **Response:** No content (204)  
    - **Errors:** 404 Not Found if employee does not exist  
    """
    employeeservice.update_employee(db, employee_id, employee_update)


@router.delete("/{employee_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_employee(
    db: db_dependency, 
    employee_id: int = Path(gt=0),
    user: dict = Depends(require_admin)
):
    """
    **Delete an employee by ID**  
    - **Requires Admin role**  
    - **Path Parameter:** `employee_id` (integer, must be greater than 0)  
    - **Response:** No content (204)  
    - **Errors:** 404 Not Found if employee does not exist  
    """
    employeeservice.delete_employee(db, employee_id)
