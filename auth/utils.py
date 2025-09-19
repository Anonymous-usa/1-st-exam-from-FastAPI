from .models import User
from database import LocalSession
from passlib.hash import bcrypt
from .schemas import UserRegisterSchema
import uuid

def hesh_password(password):
    return bcrypt.hash(password)

def verify_password(password, hashed_password):
    return bcrypt.verify(password, hashed_password)

def check_user(user: UserRegisterSchema):
    db =  LocalSession()
    user = db.query(User).filter(User.username == user.username).first()
    db.close()
    if user:
        return user
    return None