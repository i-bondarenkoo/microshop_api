from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db_session

import crud
from schemas.customer import (
    CustomerSchema,
    CreateCustomerSchema,
    UpdateCustomerSchema,
)

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post("/")
async def create_customer(
    customer_schema: CreateCustomerSchema,
    session: AsyncSession = Depends(get_db_session),
    response_model = CustomerSchema,
):
    customer = await crud.create_customer(
        session=session,
        customer_schema=customer_schema,
    )
    return customer.as_schema()


@router.get("/")
async def get_customers(
    limit: int = 20,
    offset: int = 0,
    session: AsyncSession = Depends(get_db_session),
):
    customers = await crud.get_customers(
        session=session,
        limit=limit,
        offset=offset,
    )
    if not customers:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )
    return [
        customer.as_schema()
        for customer in customers
    ]


@router.get("/{customer_id}")
async def get_customer_by_id(
    customer_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    customers = await crud.get_customers(
        session=session,
        customer_id=customer_id,
        limit=1,
        offset=0,
    )
    if not customers:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )
    return customers[0].as_schema()


@router.patch("/{customer_id}")
async def update_partial_info_customer(
    customer_schema: UpdateCustomerSchema,
    customer_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    customer = await crud.update_customer(
        session=session,
        customer_id=customer_id,
        customer_schema=customer_schema,
        clear_fields=False,
    )
    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )
    return customer.as_schema()


@router.put("/{customer_id}")
async def update_full_info_customer(
    customer_schema: UpdateCustomerSchema,
    customer_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    customer = await crud.update_customer(
        session=session,
        customer_id=customer_id,
        customer_schema=customer_schema,
        clear_fields=True,
    )
    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )
    return customer.as_schema()
