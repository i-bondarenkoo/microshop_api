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
from models.models_product import ProductOrm
from schemas.schemas_product import (
    CreateProductSchema,
    ResponseProductSchema,
    UpdateProductPartialSchema,
)


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


# ----------------------------------------------------------------
# crud product
async def create_product_crud(
    product: CreateProductSchema,
    session: AsyncSession = Depends(get_session_to_db),
    responce_model=ResponseProductSchema,
):
    new_product = ProductOrm(**product.model_dump())
    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)

    return new_product


async def get_all_products_crud(
    session: AsyncSession = Depends(get_session_to_db),
    model_response=ResponseProductSchema,
):
    stmt = select(ProductOrm).order_by(ProductOrm.id)
    result = await session.execute(stmt)
    all_products = result.scalars().all()
    return all_products


async def get_product_by_id_crud(
    product_id: int,
    session: AsyncSession = Depends(get_session_to_db),
    responce_model=ResponseProductSchema,
):
    stmt = select(ProductOrm).where(ProductOrm.id == product_id)
    result = await session.execute(stmt)
    product_by_id = result.scalars().first()
    if not product_by_id:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product_by_id


async def update_product_partial_info_crud(
    product: UpdateProductPartialSchema,
    product_id: int,
    session: AsyncSession = Depends(get_session_to_db),
    response_model=ResponseProductSchema,
):
    get_product = await session.get(ProductOrm, product_id)
    if get_product:
        for key, value in product.model_dump(
            exclude_unset=True, exclude_none=True
        ).items():
            setattr(get_product, key, value)

        await session.commit()
        await session.refresh(get_product)

        return get_product
    raise HTTPException(status_code=404, detail="Товар не найден")
