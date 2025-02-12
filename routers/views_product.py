from fastapi import APIRouter, Depends
import crud
from schemas.schemas_product import UpdateProductPartialSchema

from schemas.schemas_product import CreateProductSchema
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session_to_db

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/")
async def create_product(
    product: CreateProductSchema, session: AsyncSession = Depends(get_session_to_db)
):
    return await crud.create_product_crud(product=product, session=session)


@router.get("/")  # Оставить для списка продуктов
async def get_all_products(session: AsyncSession = Depends(get_session_to_db)):
    return await crud.get_all_products_crud(session=session)


@router.get("/{product_id}")  # Добавить параметр для ID
async def get_product_by_id(
    product_id: int, session: AsyncSession = Depends(get_session_to_db)
):
    return await crud.get_product_by_id_crud(product_id=product_id, session=session)


@router.patch("/{product_id}")
async def update_product_partial_info(
    product: UpdateProductPartialSchema,
    product_id: int,
    session: AsyncSession = Depends(get_session_to_db),
):
    return await crud.update_product_partial_info_crud(
        product=product, product_id=product_id, session=session
    )


@router.post("/{product_id}/orders/{order_id}")
async def add_product_to_multiple_orders(
    order_ids: list[int],
    product: CreateProductSchema,
    session: AsyncSession = Depends(get_session_to_db),
):
    return await crud.add_product_to_multiple_orders_crud(
        order_ids=order_ids, product=product, session=session
    )


@router.get("/list/orders")
async def get_products_ordered_more_than_once(
    session: AsyncSession = Depends(get_session_to_db),
):
    return await crud.get_products_ordered_more_than_once_crud(session=session)
