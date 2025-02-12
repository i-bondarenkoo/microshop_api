from fastapi import Depends, HTTPException
from schemas.schemas_customer import (
    CreateCustomerSchema,
    ResponseCustomerSchema,
    UpdateFullCustomerSchema,
    UpdatePartialCustomerSchema,
)
from schemas.schemas_order import (
    CreateOrderSchema,
    ResponseOrderSchema,
    UpdateOrderSchema,
)
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session_to_db
from models.models_customer import CustomerOrm
from sqlalchemy import select
from models.models_order import OrderOrm
from models.models_product import ProductOrm
from schemas.schemas_product import (
    CreateProductSchema,
    ResponseProductSchema,
    UpdateProductPartialSchema,
)
from models.associations import order_product


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
    if not get_customer:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Обновляем только переданные поля
    update_data = customer.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(get_customer, key, value)

    await session.commit()
    await session.refresh(get_customer)
    return get_customer


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
        # exclude_unset передает только заполненные поля
        for key, value in product.model_dump(exclude_unset=True).items():
            setattr(get_product, key, value)

        await session.commit()
        await session.refresh(get_product)

        return get_product
    raise HTTPException(status_code=404, detail="Товар не найден")


async def create_order_crud(
    order: CreateOrderSchema,
    session: AsyncSession = Depends(get_session_to_db),
    responce_model=ResponseOrderSchema,
):
    check_customer_id = await session.get(CustomerOrm, order.customer_id)
    if not check_customer_id:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    new_order = OrderOrm(**order.model_dump())
    session.add(new_order)
    await session.commit()
    await session.refresh(new_order)

    return new_order


async def get_all_orders_crud(
    session: AsyncSession = Depends(get_session_to_db),
    responce_model=ResponseOrderSchema,
):
    stmt = select(OrderOrm).order_by(OrderOrm.id)
    result = await session.execute(stmt)
    all_orders = result.scalars().all()
    return all_orders


async def get_order_by_id_crud(
    order_id: int,
    session: AsyncSession = Depends(get_session_to_db),
    responce_model=ResponseOrderSchema,
):
    stmt = select(OrderOrm).where(OrderOrm.id == order_id)
    result = await session.execute(stmt)
    order_by_id = result.scalars().one_or_none()
    if not order_by_id:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return order_by_id


async def delete_order_crud(
    order_id: int, session: AsyncSession = Depends(get_session_to_db)
):
    # Находим заказ по ID
    stmt = select(OrderOrm).where(OrderOrm.id == order_id)
    result = await session.execute(stmt)
    order = result.scalar_one_or_none()

    # Если не найден — возвращаем 404
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")

    # Удаляем заказ
    await session.delete(order)
    await session.commit()

    return {"message": "Заказ успешно удален"}


async def add_product_to_order_crud(
    product_id: int, order_id: int, session: AsyncSession = Depends(get_session_to_db)
):
    # Находим заказ и продукт по id
    order = await session.get(OrderOrm, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    product = await session.get(ProductOrm, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    # Добавляем продукт к заказу
    stmt = order_product.insert().values(order_id=order_id, product_id=product_id)
    await session.execute(stmt)
    await session.commit()

    return {"message": "Продукт успешно добавлен в заказ"}


async def get_info_about_order_crud(
    order_id: int, session: AsyncSession = Depends(get_session_to_db)
):
    # Загружаем заказ по ID
    order = await session.get(OrderOrm, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")

    stmt = (
        select(OrderOrm)
        .where(OrderOrm.id == order_id)
        .options(selectinload(OrderOrm.customer), selectinload(OrderOrm.products))
    )

    result = await session.execute(stmt)
    order_with_customer_and_products = result.scalars().one_or_none()

    if not order_with_customer_and_products:
        raise HTTPException(status_code=404, detail="Заказ не найден")

    return order_with_customer_and_products
