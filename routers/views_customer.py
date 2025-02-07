from fastapi import APIRouter, Depends
import crud
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.schemas_customer import (
    CreateCustomerSchema,
    UpdatePartialCustomerSchema,
    UpdateFullCustomerSchema,
)
from database import get_session_to_db

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post("/")
async def create_customer(
    customer: CreateCustomerSchema, session: AsyncSession = Depends(get_session_to_db)
):
    return await crud.create_customer_crud(session=session, customer=customer)


@router.get("/")
async def get_customers(session: AsyncSession = Depends(get_session_to_db)):
    return await crud.get_all_customers_crud(session=session)


@router.get("/{customer_id}")
async def get_customer_by_id(
    customer_id: int, session: AsyncSession = Depends(get_session_to_db)
):
    return await crud.get_customer_by_id_crud(session=session, customer_id=customer_id)


@router.patch("/{customer_id}")
async def update_partial_info_customer(
    customer: UpdatePartialCustomerSchema,
    customer_id: int,
    session: AsyncSession = Depends(get_session_to_db),
):
    return await crud.update_partial_info_customer_crud(
        customer=customer, customer_id=customer_id, session=session
    )


@router.put("/{customer_id}")
async def update_full_info_customer(
    customer: UpdateFullCustomerSchema,
    customer_id: int,
    session: AsyncSession = Depends(get_session_to_db),
):
    return await crud.update_full_info_customer_crud(
        customer=customer, customer_id=customer_id, session=session
    )
