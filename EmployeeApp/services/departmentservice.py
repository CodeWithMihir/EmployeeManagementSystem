from sqlalchemy.orm import Session
from fastapi import HTTPException
from http import HTTPStatus
from models import Department
import schemas

def create_department(db: Session, newDeptRequest: schemas.DepartmentCreate):
    """Creates a new department if it doesn't already exist."""
    existing_dept = db.query(Department).filter(Department.name == newDeptRequest.name).first()
    if existing_dept:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Department '{newDeptRequest.name}' already exists."
        )

    deptModel = Department(**newDeptRequest.model_dump())
    db.add(deptModel)
    db.commit()
    db.refresh(deptModel)
    return {"message": "Department created successfully", "department": deptModel}


def get_all_departments(db: Session):
    """Retrieves all departments."""
    return db.query(Department).all()


def get_department_by_id(db: Session, departmentId: int):
    """Fetches a department by ID."""
    dept_model = db.query(Department).filter(Department.id == departmentId).first()
    if dept_model is not None:
        return dept_model
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Department not found.")


def update_department(db: Session, departmentId: int, deptUpdateRequest: schemas.DepartmentCreate):
    """Updates an existing department."""
    deptModel = db.query(Department).filter(Department.id == departmentId).first()

    if deptModel is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Department not found.")

    deptModel.name = deptUpdateRequest.name
    deptModel.description = deptUpdateRequest.description
    db.add(deptModel)
    db.commit()
    return {"message": "Department updated successfully"}


def delete_department(db: Session, departmentId: int):
    """Deletes a department by ID."""
    deptModel = db.query(Department).filter(Department.id == departmentId).first()
    if deptModel is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Department not found.")

    db.query(Department).filter(Department.id == departmentId).delete(synchronize_session=False)
    db.commit()
    return {"message": "Department deleted successfully"}
