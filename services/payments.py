from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from uuid import UUID

from models.payments import Payment, PaymentStatus, PaymentMethod  # adjust import as needed


class PaymentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_payment(
        self,
        order_id: str,
        method: PaymentMethod,
        amount: float,
        currency: str,
        user_id: Optional[str] = None,
        transaction_id: Optional[str] = None,
        gateway_response: Optional[str] = None,
        status: PaymentStatus = PaymentStatus.Pending,
        parent_payment_id: Optional[str] = None,
        refunded_amount: float = 0.0,
    ) -> Payment:
        payment = Payment(
            order_id=order_id,
            method=method,
            amount=amount,
            currency=currency,
            user_id=user_id,
            transaction_id=transaction_id,
            gateway_response=gateway_response,
            status=status,
            parent_payment_id=parent_payment_id,
            refunded_amount=refunded_amount,
        )
        self.db.add(payment)
        await self.db.flush()  # flush to get ID if needed
        return payment

    async def get_payment(self, payment_id: str) -> Optional[Payment]:
        result = await self.db.execute(select(Payment).where(Payment.id == payment_id))
        return result.scalars().first()

    async def update_payment(
        self,
        payment_id: str,
        **kwargs
    ) -> Optional[Payment]:
        # Fetch existing payment
        payment = await self.get_payment(payment_id)
        if not payment:
            return None

        # Update attributes
        for key, value in kwargs.items():
            if hasattr(payment, key):
                setattr(payment, key, value)

        await self.db.flush()
        return payment

    async def delete_payment(self, payment_id: str) -> bool:
        result = await self.db.execute(delete(Payment).where(Payment.id == payment_id))
        await self.db.flush()
        return result.rowcount > 0

    async def list_payments_for_order(self, order_id: str) -> List[Payment]:
        result = await self.db.execute(select(Payment).where(Payment.order_id == order_id))
        return result.scalars().all()
