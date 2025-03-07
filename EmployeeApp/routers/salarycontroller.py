from typing import Annotated
from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from database import get_db
from routers.auth import get_current_user, require_admin, require_manager
import schemas
from services import salaryservice  # Import the service layer
from http import HTTPStatus

router = APIRouter(tags=["Salary Management"])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.post("/salary", response_model=schemas.SalaryResponse, status_code=HTTPStatus.CREATED)
def create_salary(
    salary: schemas.SalaryCreate,
    db: db_dependency,
    user: dict = Depends(require_manager)
):
    """
    **Create a new salary record for an employee**  
    - **Requires Manager role**  
    - **Request Body:** Salary details (`SalaryCreate` schema)  
    - **Response:** Newly created salary record (`SalaryResponse` schema)  
    - **Status Code:** 201 Created  
    - **Errors:**  
      - 403 Forbidden: If the employee already has an existing salary  
    """
    return salaryservice.create_salary(db, salary)

@router.get("/salary/{employee_id}", response_model=schemas.SalaryResponse, status_code=HTTPStatus.OK)
def get_salary_by_employee_id(
    db: db_dependency,
    user: user_dependency,
    employee_id: int = Path(gt=0)
):
    """
    **Retrieve salary details for a specific employee**  
    - **Requires Authentication**  
    - **Path Parameter:** `employee_id` (integer, must be greater than 0)  
    - **Response:** Employee salary details (`SalaryResponse` schema)  
    - **Status Code:** 200 OK  
    - **Errors:**  
      - 404 Not Found: If salary record does not exist for the given employee  
    """
    return salaryservice.get_salary_by_employee_id(db, employee_id)

@router.put("/salary/{employee_id}", response_model=schemas.SalaryResponse, status_code=HTTPStatus.OK)
def update_salary(
    db: db_dependency,
    employee_id: int = Path(gt=0),
    increment: float = 0,
    user: dict = Depends(require_manager)
):
    """
    **Update an employee's salary by applying an increment**  
    - **Requires Manager role**  
    - **Path Parameter:** `employee_id` (integer, must be greater than 0)  
    - **Query Parameter:** `incrementt` (float, default is 0)  
    - **Response:** Updated salary record (`SalaryResponse` schema)  
    - **Status Code:** 200 OK  
    - **Errors:**  
      - 404 Not Found: If salary record does not exist for the given employee  
    """
    return salaryservice.update_salary(db, employee_id, increment)

@router.delete("/salary/{employee_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_salary(
    db: db_dependency,
    employee_id: int = Path(gt=0),
    user: dict = Depends(require_admin)
):
    """
    **Delete an employee's salary record**  
    - **Requires Admin role**  
    - **Path Parameter:** `employee_id` (integer, must be greater than 0)  
    - **Response:** No content (204)  
    - **Errors:**  
      - 404 Not Found: If salary record does not exist for the given employee  
    """
    return salaryservice.delete_salary(db, employee_id)
