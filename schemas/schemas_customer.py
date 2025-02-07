from ast import Pass
from pydantic import BaseModel, EmailStr
from datetime import datetime


class CreateCustomerSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: int


class ResponseCustomerSchema(CreateCustomerSchema):
    id: int


class UpdatePartialCustomerSchema(CreateCustomerSchema):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    phone_number: int | None = None


class UpdateFullCustomerSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: int
