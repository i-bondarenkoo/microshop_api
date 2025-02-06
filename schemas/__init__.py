__all__ = (
    "CreateCustomerSchema",
    "ResponceCustomerSchema",
    "UpdateCustomerSchema",
    "CreateOrderSchema",
    "CreateProductSchema",
    "UpdateProductSchema",
    "ResponceProductSchema",
    "ResponseOrderSchema",
    "UpdateOrderSchema",
)

from .schemas_customer import (
    CreateCustomerSchema,
    ResponceCustomerSchema,
    UpdateCustomerSchema,
)

from .schemas_order import CreateOrderSchema, ResponseOrderSchema, UpdateOrderSchema
from .schemas_product import (
    CreateProductSchema,
    UpdateProductSchema,
    ResponceProductSchema,
)
