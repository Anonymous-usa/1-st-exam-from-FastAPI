from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import BaseModel
from datetime import datetime

# Product (Телефон): id, name, description, price, image, created_at
class Product(BaseModel):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    name: Mapped[str] = mapped_column(String(40), nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    image: Mapped[str] = mapped_column(String(255), nullable=False) 
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    
    carts: Mapped[list["Cart"]] = relationship("Cart", back_populates="product")
