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
from sqlalchemy import func
from datetime import datetime


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


# Напиши запрос, который извлекает все заказы, сделанные пользователем,
# сортируя их по дате создания (например, от самых новых к самым старым).
# Выведи ID заказов, дату создания и общую стоимость для каждого заказа.
async def get_all_orders_by_customer_id_crud(
    customer_id: int,
    session: AsyncSession = Depends(get_session_to_db),
):
    customer = await session.get(CustomerOrm, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    stmt = (
        select(OrderOrm.id, OrderOrm.created_at, OrderOrm.total_price)
        .where(OrderOrm.customer_id == customer_id)
        .order_by(OrderOrm.created_at.desc())
    )

    result = await session.execute(stmt)
    orders_by_customer = result.all()

    return [
        {"id": obj[0], "created_at": obj[1], "total_price": obj[2]}
        for obj in orders_by_customer
    ]


#     3. Добавление продукта в несколько заказов
# Создай функцию, которая добавляет один и тот же продукт в несколько заказов.
# Продукт должен добавляться к заказам, переданным в запросе.
async def add_product_to_multiple_orders_crud(
    order_ids: list[int],
    product: CreateProductSchema,
    session: AsyncSession = Depends(get_session_to_db),
):
    # Проверяем, существуют ли все заказы
    order_stmt = select(OrderOrm.id).where(OrderOrm.id.in_(order_ids))
    result = await session.execute(order_stmt)
    existing_orders = {row for row in result.scalars().all()}  # Преобразуем в множество

    if len(existing_orders) != len(order_ids):
        raise HTTPException(
            status_code=404, detail="Один или несколько заказов не найдены"
        )

    # Создаем новый продукт
    new_product = ProductOrm(**product.model_dump())
    session.add(new_product)
    await session.commit()  # Фиксируем добавление продукта
    await session.refresh(new_product)  # Получаем его ID

    # Подготавливаем данные для массовой вставки
    insert_values = [
        {"order_id": order_id, "product_id": new_product.id} for order_id in order_ids
    ]

    # Выполняем массовую вставку
    if insert_values:
        stmt = order_product.insert().values(insert_values)
        await session.execute(stmt)
        await session.commit()

    return {"message": "Продукт успешно добавлен в заказы"}


# 4. Получение продуктов, которые были заказаны более одного раза
# Напиши запрос, который возвращает все продукты, которые были заказаны более одного раза.
# Для каждого продукта выведи количество заказов, в которых он присутствует.
async def get_products_ordered_more_than_once_crud(
    session: AsyncSession = Depends(get_session_to_db),
):
    # выбираем product_id из таблицы связи order_product и считаем количество заказов для каждого продукта с помощью func.count().
    stmt = (
        select(
            order_product.c.product_id,
            func.count(order_product.c.order_id).label("количество заказов"),
        )
        .group_by(order_product.c.product_id)
        .having(func.count(order_product.c.order_id) > 1)
    )

    result = await session.execute(stmt)
    products = result.fetchall()

    return [
        {"product_id": product[0], "количество заказов": product[1]}
        for product in products
    ]


# 5. Суммирование стоимости заказов для каждого пользователя
# Напиши запрос, который извлекает список всех пользователей с суммой стоимости их заказов.
# Для каждого пользователя выведи его имя и общую стоимость всех заказов.


async def get_users_with_total_order_price_crud(
    session: AsyncSession = Depends(get_session_to_db),
):
    stmt = (
        select(
            CustomerOrm.first_name,
            func.coalesce(func.sum(OrderOrm.total_price), 0).label("total_order_price"),
        )
        .join(OrderOrm, CustomerOrm.id == OrderOrm.customer_id, isouter=True)
        .group_by(CustomerOrm.id)
    )

    result = await session.execute(stmt)
    users_with_total_order_price = result.all()

    return [
        {"first_name": user[0], "total_order_price": user[1]}
        for user in users_with_total_order_price
    ]


# 6. Поиск заказов по определенному диапазону дат
# Напиши запрос, который извлекает все заказы, сделанные в определенный промежуток времени.
# Запрос должен позволять передавать начальную и конечную даты.


async def get_orders_by_date_range_crud(
    start_date: str,
    end_date: str,
    session: AsyncSession = Depends(get_session_to_db),
):
    start_date = datetime.strptime(start_date.strip(), "%d-%m-%Y %H:%M:%S")
    end_date = datetime.strptime(end_date.strip(), "%d-%m-%Y %H:%M:%S")

    stmt = select(OrderOrm).where(
        OrderOrm.created_at >= start_date, OrderOrm.created_at <= end_date
    )
    result = await session.execute(stmt)
    orders_by_date_range = result.scalars().all()
    return orders_by_date_range
