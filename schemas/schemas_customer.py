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


class UpdatePartialCustomerSchema(BaseModel):
    first_name: str | None
    last_name: str | None
    email: EmailStr | None
    phone_number: int | None


class UpdateFullCustomerSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: int
