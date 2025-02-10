from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from database import Base

import schemas.customer as schemas

from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
    from models.order import Order


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(50), unique=True)
    phone_number: Mapped[str] = mapped_column(String(15), nullable=True)

    orders: Mapped[list["Order"]] = relationship(
        "Order", back_populates="customer"
    )

    @classmethod
    def from_schema(cls, schema: schemas.BaseCustomerSchema) -> "Customer":
        return cls(
            **cls.__map_schema_fields(
                schema=schema,
                filter_empty=False,
            ),
        )


    def as_schema(self) -> schemas.CustomerSchema:
        return schemas.CustomerSchema(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            phone_number=self.phone_number,
        )


    def update_by_schema(
        self,
        schema: schemas.UpdateCustomerSchema,
        filter_empty: bool,
    ):
        mapping = self.__map_schema_fields(
            schema=schema,
            filter_empty=filter_empty,
        )
        for field, value in mapping.items(): # кринж, но лучше пока не придумал
            setattr(self, field, value)


    @classmethod
    def __map_schema_fields(
        cls,
        schema: schemas.BaseCustomerSchema,
        filter_empty: bool,
    ) -> dict[str, Any]:
        mapping = {
            'first_name': schema.first_name,
            'last_name': schema.last_name,
            'email': schema.email,
            'phone_number': schema.phone_number,
        }
        if not filter_empty:
            for key, value in mapping.items():
                if value is None:
                    mapping.pop(key)
        return mapping
