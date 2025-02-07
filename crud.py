from fastapi import Depends, HTTPException
from schemas.schemas_customer import (
    CreateCustomerSchema,
    ResponseCustomerSchema,
    UpdateFullCustomerSchema,
    UpdatePartialCustomerSchema,
)
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session_to_db
from models.models_customer import CustomerOrm
from sqlalchemy import select


async def create_customer_crud(
    customer: CreateCustomerSchema,
    session: AsyncSession = Depends(get_session_to_db),
    responce_model=ResponseCustomerSchema,
):
    new_customer = CustomerOrm(**customer.model_dump())
    session.add(new_customer)
    await session.commit()
    await session.refresh(new_customer)
    return new_customer


async def get_all_customers_crud(
    session: AsyncSession = Depends(get_session_to_db),
    responce_model=ResponseCustomerSchema,
):
    stmt = select(CustomerOrm).order_by(CustomerOrm.id)
    result = await session.execute(stmt)
    all_customers = result.scalars().all()
    return all_customers


async def get_customer_by_id_crud(
    customer_id: int,
    session: AsyncSession = Depends(get_session_to_db),
    responce_model=ResponseCustomerSchema,
):
    stmt = select(CustomerOrm).where(CustomerOrm.id == customer_id)
    result = await session.execute(stmt)
    customer_by_id = result.scalars().one_or_none()
    if not customer_by_id:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return customer_by_id


async def update_partial_info_customer_crud(
    customer: UpdatePartialCustomerSchema,
    customer_id: int,
    session: AsyncSession = Depends(get_session_to_db),
    response_model=ResponseCustomerSchema,
):
    get_customer = await session.get(CustomerOrm, customer_id)
    if get_customer:
        # Обновляем только переданные поля
        for key, value in customer.model_dump(exclude_unset=True).items():
            setattr(get_customer, key, value)
        await session.commit()
        await session.refresh(get_customer)
        return get_customer
    raise HTTPException(status_code=404, detail="Пользователь не найден")


async def update_full_info_customer_crud(
    customer: UpdateFullCustomerSchema,
    customer_id: int,
    session: AsyncSession = Depends(get_session_to_db),
    response_model=ResponseCustomerSchema,
):
    # orm object get_customer
    get_customer = await session.get(CustomerOrm, customer_id)
    if not get_customer:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    # customer - pydantic object
    # customer.model_dump() Pydantic -> dict
    for key, value in customer.model_dump(exclude_unset=True).items():
        # обновляем orm object данными из pydantic object преобразованными в dict
        setattr(get_customer, key, value)

    await session.commit()
    # все еще orm object в БД
    await session.refresh(get_customer)
    # за счет responce model преобразуем orm object в pydantic object
    return get_customer
