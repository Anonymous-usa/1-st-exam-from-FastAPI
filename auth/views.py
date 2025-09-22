from fastapi import APIRouter, Depends, status, HTTPException
from database import get_db
from sqlalchemy.orm import Session

from .models import User
from .schemas import UserSchema, UserRegisterSchema, UserLoginSchema
from .utils import check_user, hesh_password, verify_password
from .handlers import  generate_token, decode_jwt, JWTBearer

auth_router = APIRouter()

@auth_router.post("/register", response_model=UserSchema, status_code = status.HTTP_201_CREATED)
async def user_register(user_data: UserRegisterSchema, db: Session = Depends(get_db)):
    is_user_exists = check_user(user_data)
    
    if is_user_exists:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "User alredy exists")
    password_hash = hesh_password(user_data.password)
    print(user_data)
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
    

@auth_router.delete("/delete", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())], summary="Delete a user")
async def delete_user(db: Session = Depends(get_db), token: str = Depends(JWTBearer())):
    decoded_token = decode_jwt(token)
    if "user_id" not in decoded_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    user_id = decoded_token["user_id"]
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

@auth_router.post("/logout", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())], summary="Logout a user")
async def logout_user():
    return {"message": "User logged out successfully"}

@auth_router.get("/me", status_code=status.HTTP_200_OK, response_model=UserSchema, dependencies=[Depends(JWTBearer())])
async def get_current_user(db: Session = Depends(get_db), token: str = Depends(JWTBearer())):
    decoded_token = decode_jwt(token)
    if "user_id" not in decoded_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user_id = decoded_token["user_id"]
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user





