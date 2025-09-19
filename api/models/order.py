from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import BaseModel
from datetime import datetime

def get_user():
    from auth.models import User
    return User

# Order (Заказ): id, user, total_amount, created_at, status
class Order(BaseModel):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="orders")

    total_amount: Mapped[float] = mapped_column(Integer, nullable=False) 
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)
