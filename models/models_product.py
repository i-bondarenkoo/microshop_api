from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, Integer
from database import Base


class ProductOrm(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)  # название товара
    description: Mapped[str] = mapped_column(
        String(255), nullable=True
    )  # описание товара
    price: Mapped[float] = mapped_column(Float, nullable=False)  # цена товара
    stock_quantity: Mapped[int] = mapped_column(
        Integer, nullable=False
    )  # количество товара на складе
