from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from models.orders import Order, OrderItem, OrderStatus  # adjust imports
from services.orders import OrderService, OrderItemService  # adjust imports
from core.database import get_db  # your async session dependency

router = APIRouter(prefix="/api/v1/orders", tags=["Orders"])

# --- Order Routes --- #

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_order(
    user_id: str,
    total_amount: float,
    currency: str = "USD",
    status: OrderStatus = OrderStatus.Pending,
    items: List[dict] = [],
    db: AsyncSession = Depends(get_db),
):
    service = OrderService(db)
    order = await service.create_order(user_id, total_amount, currency, status, items)
    return order.to_dict()

@router.get("/{order_id}", response_model=dict)
async def get_order(order_id: str, db: AsyncSession = Depends(get_async_db)):
    service = OrderService(db)
    order = await service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order.to_dict()

@router.put("/{order_id}", response_model=dict)
async def update_order(order_id: str, update_data: dict, db: AsyncSession = Depends(get_async_db)):
    service = OrderService(db)
    order = await service.update_order(order_id, **update_data)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order.to_dict()

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: str, db: AsyncSession = Depends(get_async_db)):
    service = OrderService(db)
    deleted = await service.delete_order(order_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Order not found")
    return

@router.get("/user/{user_id}", response_model=List[dict])
async def list_orders_for_user(user_id: str, db: AsyncSession = Depends(get_async_db)):
    service = OrderService(db)
    orders = await service.list_orders_for_user(user_id)
    return [order.to_dict() for order in orders]


# --- Order Item Routes --- #

item_router = APIRouter(prefix="/order-items", tags=["Order Items"])

@item_router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_order_item(
    order_id: str,
    product_id: str,
    quantity: int,
    price_per_unit: float,
    db: AsyncSession = Depends(get_async_db),
):
    service = OrderItemService(db)
    item = await service.create_order_item(order_id, product_id, quantity, price_per_unit)
    return item.to_dict()

@item_router.get("/{item_id}", response_model=dict)
async def get_order_item(item_id: str, db: AsyncSession = Depends(get_async_db)):
    service = OrderItemService(db)
    item = await service.get_order_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Order item not found")
    return item.to_dict()

@item_router.put("/{item_id}", response_model=dict)
async def update_order_item(item_id: str, update_data: dict, db: AsyncSession = Depends(get_async_db)):
    service = OrderItemService(db)
    item = await service.update_order_item(item_id, **update_data)
    if not item:
        raise HTTPException(status_code=404, detail="Order item not found")
    return item.to_dict()

@item_router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order_item(item_id: str, db: AsyncSession = Depends(get_async_db)):
    service = OrderItemService(db)
    deleted = await service.delete_order_item(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Order item not found")
    return

@item_router.get("/order/{order_id}", response_model=List[dict])
async def list_items_for_order(order_id: str, db: AsyncSession = Depends(get_async_db)):
    service = OrderItemService(db)
    items = await service.list_items_for_order(order_id)
    return [item.to_dict() for item in items]
