from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from database import Base


class CustomerOrm(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(50), unique=True)
    phone_number: Mapped[int] = mapped_column(String(15), nullable=True)

    orders: Mapped[list["OrderOrm"]] = relationship(
        "OrderOrm", back_populates="customer"
    )
