from database import Base
from sqlalchemy import Table, Column, Integer, ForeignKey

# Сводная таблица многие ко многим заказы/продукты
order_product = Table(
    "order_product",
    Base.metadata,
    Column("order_id", Integer, ForeignKey("orders.id"), primary_key=True),
    Column("product_id", Integer, ForeignKey("products.id"), primary_key=True),
)
