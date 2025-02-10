from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, ForeignKey, Date
from database import Base
from .associations import order_product
from datetime import datetime


class OrderOrm(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("customers.id"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow
    )

    total_price: Mapped[int] = mapped_column(Float, nullable=False)
    payment_method: Mapped[str] = mapped_column(String(20), nullable=False)

    # Отложенные аннотации, чтобы избежать циклического импорта
    customer: Mapped["CustomerOrm"] = relationship(
        "CustomerOrm", back_populates="orders"
    )
    products: Mapped[list["ProductOrm"]] = relationship(
        "ProductOrm", secondary=order_product, back_populates="orders"
    )
