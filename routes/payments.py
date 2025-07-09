from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from models.payments import Payment, PaymentMethod, PaymentStatus  # adjust imports
from services.payments import PaymentService  # async service for payments
from core.database import get_db  # async session dependency

router = APIRouter(prefix="/api/v1/payments", tags=["Payments"])


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_payment(
    order_id: str,
    amount: float,
    currency: str,
    method: PaymentMethod,
    user_id: Optional[str] = None,
    transaction_id: Optional[str] = None,
    gateway_response: Optional[str] = None,
    parent_payment_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    service = PaymentService(db)
    payment = await service.create_payment(
        order_id=order_id,
        amount=amount,
        currency=currency,
        method=method,
        user_id=user_id,
        transaction_id=transaction_id,
        gateway_response=gateway_response,
        parent_payment_id=parent_payment_id,
    )
    return payment.to_dict()


@router.get("/{payment_id}", response_model=dict)
async def get_payment(payment_id: str, db: AsyncSession = Depends(get_async_db)):
    service = PaymentService(db)
    payment = await service.get_payment(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment.to_dict()


@router.put("/{payment_id}", response_model=dict)
async def update_payment(payment_id: str, update_data: dict, db: AsyncSession = Depends(get_async_db)):
    service = PaymentService(db)
    payment = await service.update_payment(payment_id, **update_data)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment.to_dict()


@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_payment(payment_id: str, db: AsyncSession = Depends(get_async_db)):
    service = PaymentService(db)
    deleted = await service.delete_payment(payment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Payment not found")
    return


@router.get("/order/{order_id}", response_model=List[dict])
async def list_payments_for_order(order_id: str, db: AsyncSession = Depends(get_async_db)):
    service = PaymentService(db)
    payments = await service.list_payments_for_order(order_id)
    return [payment.to_dict() for payment in payments]


@router.get("/user/{user_id}", response_model=List[dict])
async def list_payments_for_user(user_id: str, db: AsyncSession = Depends(get_async_db)):
    service = PaymentService(db)
    payments = await service.list_payments_for_user(user_id)
    return [payment.to_dict() for payment in payments]
