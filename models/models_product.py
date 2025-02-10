from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float, Integer
from database import Base
from .associations import order_product


class ProductOrm(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(255))
    price: Mapped[float]
    quantity: Mapped[int]

    # Используем строки в relationship, чтобы избежать циклического импорта
    orders: Mapped[list["OrderOrm"]] = relationship(
        "OrderOrm", secondary=order_product, back_populates="products"
    )
