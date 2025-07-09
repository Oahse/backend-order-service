from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class OrderStatus(str, Enum):
    Pending = "Pending"
    Processing = "Processing"
    Shipped = "Shipped"
    Delivered = "Delivered"
    Cancelled = "Cancelled"
    Returned = "Returned"
    Failed = "Failed"


class OrderItemSchema(BaseModel):
    id: str
    order_id: str
    product_id: str
    quantity: int
    price_per_unit: float
    total_price: float

    class Config:
        from_attributes = True


class OrderSchema(BaseModel):
    id: str
    user_id: str
    status: OrderStatus
    total_amount: float
    currency: str = Field(default="USD")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    items: List[OrderItemSchema] = []

    class Config:
        from_attributes = True
