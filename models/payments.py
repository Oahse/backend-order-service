from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, DateTime, Enum, Integer, Boolean, DECIMAL, Text
from enum import Enum as PyEnum
from datetime import datetime
from typing import Optional
from uuid import uuid4
from core.database import Base, CHAR_LENGTH


class PaymentMethod(PyEnum):
    CreditCard = "CreditCard"
    DebitCard = "DebitCard"
    BankTransfer = "BankTransfer"
    Paypal = "Paypal"
    ApplePay = "ApplePay"
    GooglePay = "GooglePay"
    CashOnDelivery = "CashOnDelivery"
    Crypto = "Crypto"
    Other = "Other"


class PaymentStatus(PyEnum):
    Pending = "Pending"
    Completed = "Completed"
    Failed = "Failed"
    Refunded = "Refunded"
    Cancelled = "Cancelled"
    Authorized = "Authorized"
    Voided = "Voided"


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[str] = mapped_column(String(CHAR_LENGTH), primary_key=True, default=lambda: str(uuid4()))
    order_id: Mapped[str] = mapped_column(ForeignKey("orders.id"), nullable=False)
    order = relationship("Order", back_populates="payments")

    user_id: Mapped[Optional[str]] = mapped_column(String(CHAR_LENGTH), nullable=True)

    method: Mapped[PaymentMethod] = mapped_column(Enum(PaymentMethod), nullable=False)
    status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus), default=PaymentStatus.Pending, nullable=False)

    amount: Mapped[DECIMAL] = mapped_column(DECIMAL(18, 8), nullable=False)  # high precision for currency
    currency: Mapped[str] = mapped_column(String(10), nullable=False)  # ISO 4217 e.g. USD, EUR, JPY

    transaction_id: Mapped[Optional[str]] = mapped_column(String(CHAR_LENGTH), nullable=True)  # from payment gateway

    # Payment gateway raw response or notes (JSON/text)
    gateway_response: Mapped[Optional[Text]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    refunded_amount: Mapped[Optional[DECIMAL]] = mapped_column(DECIMAL(18, 8), default=0)

    # For partial refunds or multiple payment attempts
    parent_payment_id: Mapped[Optional[str]] = mapped_column(String(CHAR_LENGTH), ForeignKey("payments.id"), nullable=True)
    parent_payment = relationship("Payment", remote_side=[id])
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "order_id": self.order_id,
            "user_id": self.user_id,
            "method": self.method.value if self.method else None,
            "status": self.status.value if self.status else None,
            "amount": float(self.amount) if self.amount is not None else None,
            "currency": self.currency,
            "transaction_id": self.transaction_id,
            "gateway_response": self.gateway_response,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "refunded_amount": float(self.refunded_amount) if self.refunded_amount is not None else 0,
            "parent_payment_id": self.parent_payment_id,
            # Optional: if you want to include minimal parent payment info:
            "parent_payment": {"id": self.parent_payment.id} if self.parent_payment else None
        }
    def __repr__(self):
        return f"<Payment(id={self.id}, order_id={self.order_id}, method={self.method}, status={self.status}, amount={self.amount} {self.currency})>"
