from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, ForeignKey
from database import Base
from .associations import order_product


class OrderOrm(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("customers.id"), nullable=False
    )
    total_price: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending")

    # Отложенные аннотации, чтобы избежать циклического импорта
    customer: Mapped["CustomerOrm"] = relationship(
        "CustomerOrm", back_populates="orders"
    )
    products: Mapped[list["ProductOrm"]] = relationship(
        "ProductOrm", secondary=order_product, back_populates="orders"
    )
