from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from database import get_db
from enums.roleenum import UserRole
from starlette import status
import schemas
from routers.auth import get_current_user, require_admin
from services import departmentservice  # Import the service layer

router = APIRouter(prefix="/department", tags=["Department Management"])

db_dependency = Annotated[Session, Depends(get_db)] 
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post("/createdepartment", status_code=status.HTTP_201_CREATED)
async def CreateDeptAsync(
    newDeptRequest: schemas.DepartmentCreate,
    db: db_dependency,
    user: dict = Depends(require_admin),
):
    """
    **Create a new department**  
    - **Requires Admin role**  
    - **Request Body:** Department details (`DepartmentCreate` schema)  
    - **Response:** Created department  
    - **Status Code:** 201 Created  
    """
    return departmentservice.create_department(db, newDeptRequest)


@router.get("", status_code=status.HTTP_200_OK)
async def GetAllDeptAsync(user: user_dependency, db: db_dependency):
    """
    **Retrieve all departments**  
    - **Requires Authentication**  
    - **Response:** List of all departments  
    - **Status Code:** 200 OK  
    """
    return departmentservice.get_all_departments(db)


@router.get("/{departmentId}", status_code=status.HTTP_200_OK)
async def GetDeptByIdAsync(user: user_dependency, db: db_dependency, departmentId: int = Path(gt=0)):
    """
    **Retrieve a department by ID**  
    - **Requires Authentication**  
    - **Path Parameter:** `departmentId` (integer, must be greater than 0)  
    - **Response:** Department details  
    - **Status Code:** 200 OK  
    - **Errors:** 404 Not Found if department does not exist  
    """
    return departmentservice.get_department_by_id(db, departmentId)


@router.put("/{departmentId}", status_code=status.HTTP_204_NO_CONTENT)
async def UpdateDeptAsync(
    db: db_dependency,
    deptUpdateRequest: schemas.DepartmentCreate,
    departmentId: int = Path(gt=0),
    user: dict = Depends(require_admin),
):
    """
    **Update an existing department**  
    - **Requires Admin role**  
    - **Path Parameter:** `departmentId` (integer, must be greater than 0)  
    - **Request Body:** Updated department details (`DepartmentCreate` schema)  
    - **Response:** No content (204)  
    - **Errors:** 404 Not Found if department does not exist  
    """
    return departmentservice.update_department(db, departmentId, deptUpdateRequest)


@router.delete("/{departmentId}", status_code=status.HTTP_204_NO_CONTENT)
async def DeleteDeptAsync(db: db_dependency, departmentId: int = Path(gt=0), user: dict = Depends(require_admin)):
    """
    **Delete a department by ID**  
    - **Requires Admin role**  
    - **Path Parameter:** `departmentId` (integer, must be greater than 0)  
    - **Response:** No content (204)  
    - **Errors:** 404 Not Found if department does not exist  
    """
    return departmentservice.delete_department(db, departmentId)
