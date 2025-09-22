from datetime import datetime
from pydantic import BaseModel, field_validator, model_validator
from sqlalchemy import DateTime
from auth.schemas import UserSchema
from .product import ProductSchema
from typing import Optional

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
    user: Optional[UserSchema]
    product: Optional[ProductSchema]
    quantity: int
    created_at: datetime 

    @model_validator(mode='before')
    def check_consistency(cls, values):
        # Access 'quantity' directly from the model instance (values is the instance itself)
        quantity = values.quantity  # 'values' refers to the model instance, not a dict
        if quantity is None or quantity <= 0:
            raise ValueError('Quantity must be greater than zero')
        return values
