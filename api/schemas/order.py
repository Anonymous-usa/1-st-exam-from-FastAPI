from pydantic import BaseModel, Field, condecimal, field_validator, model_validator
from datetime import datetime
from typing import List, Optional
from .product import ProductSchema
from auth.schemas import UserSchema



class OrderCreateSchema(BaseModel):
    user_id: int
    status: str
    total_amount: condecimal(max_digits=10, decimal_places=2)

    @field_validator('status')
    def validate_status(cls, v):
        valid_statuses = ['pending', 'shipped', 'completed']
        if v not in valid_statuses:
            raise ValueError(f"Invalid status. Valid statuses are: {valid_statuses}")
        return v

class OrderSchema(BaseModel):
    id: int
    user: UserSchema
    order_items: List[ProductSchema]  
    status: str
    total_amount: condecimal(max_digits=10, decimal_places=2)
    created_at: datetime

    class Config:
        orm_mode = True  

   
    @model_validator(mode='before')
    def check_total_amount(cls, values):
        total_amount = values.get('total_amount')
        if total_amount <= 0:
            raise ValueError('Total amount must be greater than zero')
        return values
