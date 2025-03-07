from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from database import get_db
import schemas
from routers.auth import get_current_user, require_admin, require_manager
from typing import Annotated, List
from services import promotionservice
from http import HTTPStatus

router = APIRouter(prefix="/promotions", tags=["Promotion Management"])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.post("/createpromotion", response_model=schemas.PromotionResponse, status_code=HTTPStatus.CREATED)
def promote_employee(
    db: db_dependency,
    promotion_data: schemas.PromotionCreate,
    user: dict = Depends(require_manager)
):
    """
    **Promote an Employee**  
    - **Requires Manager role**  
    - **Request Body:** Promotion details (`PromotionCreate` schema)  
    - **Response:** Created promotion record (`PromotionResponse` schema)  
    - **Status Code:** 201 Created  
    """
    return promotionservice.promote_employee(db, promotion_data)


@router.get("", response_model=List[schemas.PromotionResponse], status_code=HTTPStatus.OK)
def get_all_promotions(db: db_dependency, user: dict = Depends(require_admin)):
    """
    **Retrieve all promotions**  
    - **Requires Admin role**  
    - **Response:** List of promotions (`PromotionResponse` schema)  
    - **Status Code:** 200 OK  
    """
    return promotionservice.get_all_promotions(db)


@router.get("/{promotion_id}", response_model=schemas.PromotionResponse, status_code=HTTPStatus.OK)
def get_promotion_by_id(
    user: user_dependency, 
    db: db_dependency, 
    promotion_id: int = Path(gt=0)
):
    """
    **Retrieve a promotion by ID**  
    - **Requires Authentication**  
    - **Path Parameter:** `promotion_id` (integer, must be greater than 0)  
    - **Response:** Promotion details (`PromotionResponse` schema)  
    - **Status Code:** 200 OK  
    - **Errors:** 404 Not Found if promotion does not exist  
    """
    return promotionservice.get_promotion_by_id(db, promotion_id)


@router.delete("/{promotion_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_promotion(
    db: db_dependency, 
    promotion_id: int = Path(gt=0),
    user: dict = Depends(require_admin)
):
    """
    **Delete a promotion record**  
    - **Requires Admin role**  
    - **Path Parameter:** `promotion_id` (integer, must be greater than 0)  
    - **Response:** No content (204)  
    - **Errors:** 404 Not Found if promotion does not exist  
    """
    promotionservice.delete_promotion(db, promotion_id)
