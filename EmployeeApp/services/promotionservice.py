from sqlalchemy.orm import Session
from models.promotion import Promotion
from models.employee import Employee
import schemas
from datetime import datetime, timezone
from fastapi import HTTPException
from http import HTTPStatus

def promote_employee(db: Session, promotion_data: schemas.PromotionCreate):
    # Check if employee exists
    employee = db.query(Employee).filter(Employee.id == promotion_data.employee_id).first()
    if not employee:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Employee not found.")

    # Create new promotion record
    new_promotion = Promotion(
        employee_id=promotion_data.employee_id,
        new_position=promotion_data.new_position,
        promotion_date=datetime.now(timezone.utc)
    )

    # Update employee's position
    employee.position = promotion_data.new_position

    db.add(new_promotion)
    db.commit()
    db.refresh(new_promotion)

    return new_promotion

def get_all_promotions(db: Session):
    return db.query(Promotion).all()

def get_promotion_by_id(db: Session, promotion_id: int):
    promotion = db.query(Promotion).filter(Promotion.id == promotion_id).first()
    if promotion is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Promotion not found.")
    return promotion

def delete_promotion(db: Session, promotion_id: int):
    promotion = db.query(Promotion).filter(Promotion.id == promotion_id).first()
    if promotion is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Promotion not found.")

    db.delete(promotion)
    db.commit()
