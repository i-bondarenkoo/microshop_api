from pydantic import BaseModel, EmailStr
from datetime import datetime


class CreateCustomerSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    created_at: datetime = datetime.utcnow()


class ResponceCustomerSchema(CreateCustomerSchema):
    id: int


class UpdateCustomerSchema(CreateCustomerSchema):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    updated_at: datetime = datetime.utcnow()
