from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class PaymentMethod(str, Enum):
    # зададим константы для способов оплаты
    CREDIT_CARD = "credit_card"
    PAYMENT_IN_CASH = "payment_in_cash"


class CreateOrderSchema(BaseModel):
    customer_id: int
    created_at: datetime = datetime.utcnow()
    total_price: int
    payment_method: PaymentMethod


class ResponseOrderSchema(CreateOrderSchema):
    id: int
    payment_method: PaymentMethod


class UpdateOrderSchema(CreateOrderSchema):

    customer_id: int | None
    created_at: datetime = datetime.utcnow()
    total_amount: int | None
