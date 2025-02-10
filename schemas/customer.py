from pydantic import BaseModel, EmailStr


class BaseCustomerSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: int


class CreateCustomerSchema(BaseCustomerSchema):
    pass


class UpdateCustomerSchema(BaseCustomerSchema):
    first_name: str | None
    last_name: str | None
    email: EmailStr | None
    phone_number: int | None


class CustomerSchema(BaseCustomerSchema):
    id: int
