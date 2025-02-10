from __future__ import annotations

__all__ = ("Customer", "Order", "Product", "order_product")

from models.customer import Customer
from models.order import Order
from models.product import Product
from models.associations import order_product
