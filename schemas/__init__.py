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

from .schemas_customer import (
    CreateCustomerSchema,
    ResponseCustomerSchema,
    UpdatePartialCustomerSchema,
    UpdateFullCustomerSchema,
)

from .schemas_order import CreateOrderSchema, ResponseOrderSchema, UpdateOrderSchema
from .schemas_product import (
    CreateProductSchema,
    UpdateProductPartialSchema,
    ResponseProductSchema,
)
