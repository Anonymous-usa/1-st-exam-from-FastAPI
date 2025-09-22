from pydantic import BaseModel, condecimal, Field, field_validator
from fastapi import UploadFile
from datetime import datetime



class ProductCreateSchema(BaseModel):
    name: str = Field(..., max_length=100)
    description: str
    price: condecimal(max_digits=10, decimal_places=2) 

    @field_validator('price')
    def check_price(cls, v):
        if v <= 0:
            raise ValueError("Price must be greater than zero")
        return v

class ProductSchema(BaseModel):
    id: int
    name: str
    description: str
    price: condecimal(max_digits=10, decimal_places=2)
    image: str
    created_at: datetime

    class Config:
        orm_mode = True 