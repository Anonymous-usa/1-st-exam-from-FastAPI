from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from api.schemas.cart import CartCreateSchema, CartSchema
from api.models.cart import Cart
from typing import List
from auth.handlers import JWTBearer
from auth.models import User
from api.models.product import Product

from database import get_db

cart_router = APIRouter()

@cart_router.get("/", response_model=List[CartSchema], status_code=status.HTTP_200_OK, summary="Get all Cart")
async def get_all_cart(db: Session = Depends(get_db)):
    all_cart = db.query(Cart).join(Product).join(User).all()
    return all_cart

@cart_router.get("/{cart_id}", response_model=CartSchema, status_code=status.HTTP_200_OK, summary="Get Cart by ID")
async def get_cart(cart_id: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).options(joinedload(Cart.user), joinedload(Cart.product)).filter(Cart.id == cart_id).first()
    
    if not cart:
        # Instead of returning a dict, raise an HTTPException with 404 status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart with this id doesn't exist")
    
    return cart


@cart_router.post("/create", response_model=CartSchema, status_code=status.HTTP_201_CREATED, dependencies=[Depends(JWTBearer())], summary="Creating Cart")
async def create_cart(cart_data:CartCreateSchema, db:Session = Depends(get_db)):
    new_cart = Cart(user_id = cart_data.user_id, product_id = cart_data.product_id, quantity = cart_data.quantity)
    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)
    return new_cart

@cart_router.delete("/{cart_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(JWTBearer())],summary="Delete Cart")
async def delete_cart(cart_id: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Cart with this id {cart_id} not found!")
    db.delete(cart)
    db.commit()
    return {"detail": f"Cart with id {cart_id} deleted successfuly!"}

@cart_router.put("/{cart_id}", response_model=CartSchema, dependencies=[Depends(JWTBearer())], status_code=status.HTTP_200_OK, summary="Update Cart")
async def update_cart(cart_id: int, cart_data: CartCreateSchema, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Cart with this id {cart_id} not found!")
    cart.user_id = cart_data.user_id
    cart.product_id = cart_data.product_id
    cart.quantity = cart_data.quantity
    db.commit()
    db.refresh(cart)
    return cart

                      