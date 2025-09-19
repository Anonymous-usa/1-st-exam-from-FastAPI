from datetime import datetime
from pydantic import BaseModel, field_validator, model_validator
from sqlalchemy import DateTime
from auth.schemas import UserSchema
from .product import ProductSchema

class CartCreateSchema(BaseModel):
    user_id: int
    product_id: int
    quantity: int

    @field_validator('quantity', mode="before")
    def validate_quantity(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be greater than zero')
        return v


class CartSchema(BaseModel):
    id: int
    user: UserSchema
    product: ProductSchema
    quantity: int
    created_at: datetime 

    
    @model_validator(mode='before')
    def check_consistency(cls, values):
        quantity = values.get('quantity')
        if quantity is None or quantity <= 0:
            raise ValueError('Quantity must be greater than zero')
        return values
