import pytest

from sqlalchemy.ext.asyncio import AsyncSession

import crud
from models.customer import Customer
from schemas.customer import (
    CustomerSchema,
    CreateCustomerSchema,
    UpdateCustomerSchema,
)


@pytest.mark.asyncio
async def test_customer_creation(
    create_customer: CreateCustomerSchema,
    db_session: AsyncSession,
):
    customer = await crud.create_customer(
        customer_schema=create_customer,
        session=db_session,
    )

    assert customer.id is not None


@pytest.mark.asyncio
async def test_customer_retrieve(
    db_session: AsyncSession,
):
    customers = await crud.get_customers(
        session=db_session,
        limit=10,
        offset=0,
    )
    customer = customers[0]
    customers_by_id = await crud.get_customers(
        customer_id=customer.id,
        session=db_session,
        limit=1,
        offset=0,
    )

    assert len(customers_by_id) == 1
    assert customers_by_id[0].id == customer.id
    assert len(customers) > 0


@pytest.mark.asyncio
async def test_customer_full_updating(
    update_customer_full: UpdateCustomerSchema,
    db_session: AsyncSession,
):
    customers = await crud.get_customers(
        session=db_session,
        limit=10,
        offset=0,
    )
    customer = customers[0]

    customer = await crud.update_customer(
        customer_schema=update_customer_full,
        customer_id=customer.id,
        session=db_session,
        clear_fields=False,
    )
    customer_dict = customer.as_schema().model_dump()
    update_customer_dict = update_customer_full.model_dump()

    for key, value in update_customer_dict.items():
        assert customer_dict[key] == value


@pytest.mark.asyncio
async def test_customer_partial_updating(
    update_customer_partial: UpdateCustomerSchema,
    db_session: AsyncSession,
):
    customers = await crud.get_customers(
        session=db_session,
        limit=10,
        offset=0,
    )
    customer = customers[0]

    customer = await crud.update_customer(
        customer_schema=update_customer_partial,
        customer_id=customer.id,
        session=db_session,
        clear_fields=True,
    )

    customer_dict = customer.as_schema().model_dump()
    update_customer_dict = update_customer_partial.model_dump()

    for key, value in update_customer_dict.items():
        assert customer_dict[key] == value

