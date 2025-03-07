from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import  APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from enums.roleenum import UserRole
from schemas import UserCreate
from models.user import User
from passlib.context import CryptContext
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt
from http import HTTPStatus


router = APIRouter(prefix='/auth', tags=["Authentication"])

SECRET_KEY = '44801eee835b697ec1271eed7f57763a'
ALGORITHM = 'HS256'


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


# Get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: str = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Failed to Validate User.')
        return {'username': username, 'id': user_id, 'user_role': user_role}
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Failed to Validate User.')

#check if user is admin or not
def require_admin(user: dict = Depends(get_current_user)):
    if user["user_role"] != UserRole.admin.value:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return user  # Return user details if they are an admin

#check if user is manager or not
def require_manager(user: dict = Depends(get_current_user)):
    if user["user_role"] != UserRole.manager.value:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return user  # Return user details if they are an manager


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(userRequest: UserCreate, db: db_dependency):
    createUserModel = User(
        email = userRequest.email,
        username = userRequest.username,
        role = userRequest.role,
        hashed_password = bcrypt_context.hash(userRequest.password),
        is_active = True
    )
    db.add(createUserModel)
    db.commit()
    db.refresh(createUserModel)
    return createUserModel

@router.get("")
async def GetAllUsersAsync(db: db_dependency):
    return db.query(User).all()

@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Failed to Validate User.')
    
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}