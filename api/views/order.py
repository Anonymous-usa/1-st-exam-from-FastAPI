from api.schemas.order import OrderCreateSchema,OrderSchema
from api.models.order import Order

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from auth.handlers import JWTBearer
from typing import List

from database import get_db

order_router = APIRouter()

@order_router.get("/", response_model=List[OrderSchema], status_code=status.HTTP_200_OK, summary="Get all Orders")
async def get_all_orders(db: Session = Depends(get_db)):
    all_orders = db.query(Order).all()
    return all_orders

@order_router.get("/{order_id}", response_model=OrderSchema,status_code=status.HTTP_200_OK, summary="Get Order by ID")
async def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return {"error": "Order with this id doesn't exists"}
    return order

@order_router.post("/create", response_model=OrderSchema, status_code=status.HTTP_201_CREATED, dependencies=[Depends(JWTBearer())], summary="Creating Order")
async def create_order(order_data:OrderCreateSchema, db:Session = Depends(get_db)):
    new_order = Order(user_id = order_data.user_id, product_id = order_data.product_id, quantity = order_data.quantity, total_price = order_data.total_price)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

@order_router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(JWTBearer())],summary="Delete Order")
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Order with this id {order_id} not found!")
    db.delete(order)
    db.commit()
    return {"detail": f"Order with id {order_id} deleted successfuly!"}

@order_router.put("/{order_id}", response_model=OrderSchema, dependencies=[Depends(JWTBearer())], status_code=status.HTTP_200_OK, summary="Update Order")
async def update_order(order_id: int, order_data: OrderCreateSchema, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Order with this id {order_id} not found!")
    order.user_id = order_data.user_id
    order.product_id = order_data.product_id
    order.quantity = order_data.quantity
    order.total_price = order_data.total_price
    db.commit()
    db.refresh(order)
    return order

