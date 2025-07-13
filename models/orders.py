from sqlalchemy.orm import mapped_column, Mapped, relationship, validates
from sqlalchemy import Enum, Integer, String, DateTime, ForeignKey, Boolean, Text, DECIMAL, Table, Column
from core.database import Base, CHAR_LENGTH
from datetime import datetime
from enum import Enum as PyEnum
from typing import List, Optional, Dict, Any

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, DateTime, Enum, Integer, Float, Text
from datetime import datetime
from enum import Enum as PyEnum
from typing import List
from uuid import uuid4
from core.database import Base, CHAR_LENGTH

class OrderStatus(PyEnum):
    Pending = "Pending"
    Processing = "Processing"
    Shipped = "Shipped"
    Delivered = "Delivered"
    Cancelled = "Cancelled"
    Returned = "Returned"
    Failed = "Failed"




class OrderStatus(PyEnum):
    Pending = "Pending"
    Processing = "Processing"
    Shipped = "Shipped"
    Delivered = "Delivered"
    Cancelled = "Cancelled"
    Returned = "Returned"
    Failed = "Failed"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[str] = mapped_column(String(CHAR_LENGTH), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(CHAR_LENGTH), nullable=False)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.Pending, nullable=False)

    total_amount: Mapped[float] = mapped_column(nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="USD")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    items: Mapped[List["OrderItem"]] = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan", lazy="joined"
    )
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "status": self.status.value,
            "total_amount": self.total_amount,
            "currency": self.currency,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "items": [item.to_dict() for item in self.items],
        }
    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, status={self.status}, total={self.total_amount})>"


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[str] = mapped_column(String(CHAR_LENGTH), primary_key=True)
    order_id: Mapped[str] = mapped_column(ForeignKey("orders.id"), nullable=False)
    order: Mapped["Order"] = relationship("Order", back_populates="items")

    product_id: Mapped[str] = mapped_column(String(CHAR_LENGTH), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price_per_unit: Mapped[float] = mapped_column(nullable=False)

    total_price: Mapped[float] = mapped_column(nullable=False)
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "price_per_unit": self.price_per_unit,
            "total_price": self.total_price,
        }
    def __repr__(self):
        return f"<OrderItem(id={self.id}, product_id={self.product_id}, quantity={self.quantity})>"

