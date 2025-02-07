from pydantic import BaseModel


class CreateProductSchema(BaseModel):
    name: str
    description: str
    price: int
    # количество товара на складе
    quantity: int


class ResponseProductSchema(CreateProductSchema):
    id: int


class UpdateProductPartialSchema(BaseModel):

    name: str | None = None
    description: str | None = None
    price: int | None = None
    # количество товара на складе
    quantity: int | None = None
