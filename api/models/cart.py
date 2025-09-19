from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import BaseModel
from datetime import datetime


from api.models.product import Product

def get_user():
    from auth.models import User  
    return User

# Cart (Корзина): id, user, product, quantity, created_at
class Cart(BaseModel):
    __tablename__ = "carts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship("User", backref="carts")

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    product: Mapped["Product"] = relationship("Product", back_populates="carts")  

    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)  
