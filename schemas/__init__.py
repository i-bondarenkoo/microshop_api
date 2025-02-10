__all__ = (
    "CreateCustomerSchema",
    "ResponseCustomerSchema",
    "UpdatePartialCustomerSchema",
    "UpdateFullCustomerSchema",
    "CreateOrderSchema",
    "CreateProductSchema",
    "UpdateProductPartialSchema",
    "ResponseProductSchema",
    "ResponseOrderSchema",
    "UpdateOrderSchema",
)

from .customer import (
    CreateCustomerSchema,
    UpdateCustomerSchema,
    CustomerSchema,
)

from .order import CreateOrderSchema, ResponseOrderSchema, UpdateOrderSchema
from .product import (
    CreateProductSchema,
    UpdateProductPartialSchema,
    ResponseProductSchema,
)
