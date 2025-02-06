from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Float


class OrderOrm(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(
        Integer, nullable=False
    )  # внешний ключ на клиента
    total_price: Mapped[float] = mapped_column(Float, nullable=False)  # общая сумма
    status: Mapped[str] = mapped_column(
        String(20), default="pending"
    )  # статус заказа (например: pending, completed, canceled)
