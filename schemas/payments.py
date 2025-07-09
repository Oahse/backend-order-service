from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class PaymentMethod(str, Enum):
    CreditCard = "CreditCard"
    DebitCard = "DebitCard"
    BankTransfer = "BankTransfer"
    Paypal = "Paypal"
    ApplePay = "ApplePay"
    GooglePay = "GooglePay"
    CashOnDelivery = "CashOnDelivery"
    Crypto = "Crypto"
    Other = "Other"


class PaymentStatus(str, Enum):
    Pending = "Pending"
    Completed = "Completed"
    Failed = "Failed"
    Refunded = "Refunded"
    Cancelled = "Cancelled"
    Authorized = "Authorized"
    Voided = "Voided"


class ParentPaymentSchema(BaseModel):
    id: str

    class Config:
        from_attributes = True


class PaymentSchema(BaseModel):
    id: str
    order_id: str
    user_id: Optional[str] = None
    method: PaymentMethod
    status: PaymentStatus = PaymentStatus.Pending
    amount: float
    currency: str
    transaction_id: Optional[str] = None
    gateway_response: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    refunded_amount: float = 0.0
    parent_payment_id: Optional[str] = None
    parent_payment: Optional[ParentPaymentSchema] = None

    class Config:
        from_attributes = True