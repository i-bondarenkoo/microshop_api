from fastapi import Depends, HTTPException

from typing import Sequence

from schemas.customer import (
    CreateCustomerSchema,
    UpdateCustomerSchema,
    CustomerSchema,
)
from schemas.order import (
    CreateOrderSchema,
    ResponseOrderSchema,
    UpdateOrderSchema,
)
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db_session
from models.customer import Customer
from sqlalchemy import select
from models.order import Order
from models.product import Product
from schemas.product import (
    CreateProductSchema,
    ResponseProductSchema,
    UpdateProductPartialSchema,
)


async def create_customer(
    customer_schema: CreateCustomerSchema,
    session: AsyncSession,
) -> Customer:
    customer = Customer.from_schema(customer_schema)
    session.add(customer)
    await session.commit()
    await session.refresh(customer)
    return customer


async def get_customers(
    session: AsyncSession,
    limit: int,
    offset: int,
    customer_id: int | None = None,
) -> Sequence[Customer]:
    stmt = select(
        Customer,
    ).order_by(
        Customer.id,
    ).limit(
        limit,
    ).offset(
        offset,
    )
    if customer_id is not None:
        stmt = stmt.where(Customer.id == customer_id)

    result = await session.execute(stmt)
    customers = result.scalars().all()
    return customers


async def update_customer(
    session: AsyncSession,
    customer_id: int,
    customer_schema: UpdateCustomerSchema,
    clear_fields: bool,
) -> Customer | None:
    customer = await session.get(Customer, customer_id)
    if not customer:
        return None

    customer.update_by_schema(
        schema=customer_schema,
        filter_empty=not clear_fields,
    )

    await session.commit()
    await session.refresh(customer)
    return customer


# ----------------------------------------------------------------
# crud product
async def create_product_crud(
    product: CreateProductSchema,
    session: AsyncSession = Depends(get_db_session),
    responce_model=ResponseProductSchema,
):
    new_product = Product(**product.model_dump())
    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)

    return new_product


async def get_all_products_crud(
    session: AsyncSession = Depends(get_db_session),
    model_response=ResponseProductSchema,
):
    stmt = select(Product).order_by(Product.id)
    result = await session.execute(stmt)
    all_products = result.scalars().all()
    return all_products


async def get_product_by_id_crud(
    product_id: int,
    session: AsyncSession = Depends(get_db_session),
    responce_model=ResponseProductSchema,
):
    stmt = select(Product).where(Product.id == product_id)
    result = await session.execute(stmt)
    product_by_id = result.scalars().first()
    if not product_by_id:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product_by_id


async def update_product_partial_info_crud(
    product: UpdateProductPartialSchema,
    product_id: int,
    session: AsyncSession = Depends(get_db_session),
    response_model=ResponseProductSchema,
):
    get_product = await session.get(Product, product_id)
    if get_product:
        # exclude_unset передает только заполненные поля
        for key, value in product.model_dump(exclude_unset=True).items():
            setattr(get_product, key, value)

        await session.commit()
        await session.refresh(get_product)

        return get_product
    raise HTTPException(status_code=404, detail="Товар не найден")


async def create_order_crud(
    order: CreateOrderSchema,
    session: AsyncSession = Depends(get_db_session),
    responce_model=ResponseOrderSchema,
):
    new_order = Order(**order.model_dump())
    session.add(new_order)
    await session.commit()
    await session.refresh(new_order)

    return new_order


async def get_all_orders_crud(
    session: AsyncSession = Depends(get_db_session),
    responce_model=ResponseOrderSchema,
):
    stmt = select(Order).order_by(Order.id)
    result = await session.execute(stmt)
    all_orders = result.scalars().all()
    return all_orders


async def get_order_by_id_crud(
    order_id: int,
    session: AsyncSession = Depends(get_db_session),
    responce_model=ResponseOrderSchema,
):
    stmt = select(Order).where(Order.id == order_id)
    result = await session.execute(stmt)
    order_by_id = result.scalars().one_or_none()
    if not order_by_id:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return order_by_id


async def delete_order_crud(
    order_id: int, session: AsyncSession = Depends(get_db_session)
):
    # Находим заказ по ID
    stmt = select(Order).where(Order.id == order_id)
    result = await session.execute(stmt)
    order = result.scalar_one_or_none()

    # Если не найден — возвращаем 404
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")

    # Удаляем заказ
    await session.delete(order)
    await session.commit()

    return {"message": "Заказ успешно удален"}
