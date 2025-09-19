from fastapi import APIRouter, Depends, status, HTTPException
from database import get_db
from sqlalchemy.orm import Session

from .models import User
from .schemas import UserSchema, UserRegisterSchema, UserLoginSchema
from .utils import check_user, hesh_password, verify_password
from .handlers import  generate_token

auth_router = APIRouter()

@auth_router.post("/register", response_model=UserSchema, status_code = status.HTTP_201_CREATED)
async def user_register(user_data: UserRegisterSchema, db: Session = Depends(get_db)):
    is_user_exists = check_user(user_data)
    
    if is_user_exists:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "User alredy exists")
    password_hash = hesh_password(user_data.password)
    user = User(fullname = user_data.fullname, username = user_data.username,email = user_data.email, hashed_password = password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
    

@auth_router.post("/login",  status_code=status.HTTP_200_OK)
async def user_login(user_data: UserLoginSchema, db:Session = Depends(get_db)):
    user = check_user(user_data)
    if not check_user(user_data) or not verify_password(user_data.password, user.hashed_password):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")
    return generate_token(user.id)
    

    