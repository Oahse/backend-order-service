from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from uuid import UUID

from models.orders import Order, OrderItem, OrderStatus  # adjust import


class OrderService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_order(
        self,
        user_id: str,
        total_amount: float,
        currency: str = "USD",
        status: OrderStatus = OrderStatus.Pending,
        items_data: Optional[List[Dict[str, Any]]] = None,  # List of dicts with product_id, quantity, price_per_unit
    ) -> Order:
        order = Order(user_id=user_id, total_amount=total_amount, currency=currency, status=status)
        self.db.add(order)
        await self.db.flush()  # flush to get order.id

        if items_data:
            for item_data in items_data:
                item = OrderItem(
                    order_id=order.id,
                    product_id=item_data["product_id"],
                    quantity=item_data["quantity"],
                    price_per_unit=item_data["price_per_unit"],
                    total_price=item_data["quantity"] * item_data["price_per_unit"],
                )
                self.db.add(item)

        await self.db.flush()
        await self.db.refresh(order)
        return order

    async def get_order(self, order_id: str) -> Optional[Order]:
        result = await self.db.execute(select(Order).where(Order.id == order_id))
        return result.scalars().first()

    async def update_order(self, order_id: str, **kwargs) -> Optional[Order]:
        order = await self.get_order(order_id)
        if not order:
            return None

        for key, value in kwargs.items():
            if hasattr(order, key):
                setattr(order, key, value)

        await self.db.flush()
        return order

    async def delete_order(self, order_id: str) -> bool:
        result = await self.db.execute(delete(Order).where(Order.id == order_id))
        await self.db.flush()
        return result.rowcount > 0

    async def list_orders_for_user(self, user_id: str) -> List[Order]:
        result = await self.db.execute(select(Order).where(Order.user_id == user_id))
        return result.scalars().all()


class OrderItemService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_order_item(
        self,
        order_id: str,
        product_id: str,
        quantity: int,
        price_per_unit: float,
    ) -> OrderItem:
        total_price = quantity * price_per_unit
        item = OrderItem(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            price_per_unit=price_per_unit,
            total_price=total_price,
        )
        self.db.add(item)
        await self.db.flush()
        return item

    async def get_order_item(self, item_id: str) -> Optional[OrderItem]:
        result = await self.db.execute(select(OrderItem).where(OrderItem.id == item_id))
        return result.scalars().first()

    async def update_order_item(self, item_id: str, **kwargs) -> Optional[OrderItem]:
        item = await self.get_order_item(item_id)
        if not item:
            return None

        for key, value in kwargs.items():
            if hasattr(item, key):
                setattr(item, key, value)
        # If quantity or price_per_unit changed, update total_price
        if "quantity" in kwargs or "price_per_unit" in kwargs:
            item.total_price = item.quantity * item.price_per_unit

        await self.db.flush()
        return item

    async def delete_order_item(self, item_id: str) -> bool:
        result = await self.db.execute(delete(OrderItem).where(OrderItem.id == item_id))
        await self.db.flush()
        return result.rowcount > 0

    async def list_items_for_order(self, order_id: str) -> List[OrderItem]:
        result = await self.db.execute(select(OrderItem).where(OrderItem.order_id == order_id))
        return result.scalars().all()
