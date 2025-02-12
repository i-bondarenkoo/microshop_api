from fastapi import APIRouter, Depends
import crud
from schemas.schemas_order import CreateOrderSchema
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session_to_db

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.post("/")
async def create_order(
    order: CreateOrderSchema, session: AsyncSession = Depends(get_session_to_db)
):
    return await crud.create_order_crud(order=order, session=session)


@router.get("/")
async def get_all_orders(session: AsyncSession = Depends(get_session_to_db)):
    return await crud.get_all_orders_crud(session=session)


@router.get("/{order_id}")
async def get_order_by_id(
    order_id: int, session: AsyncSession = Depends(get_session_to_db)
):
    return await crud.get_order_by_id_crud(order_id=order_id, session=session)


@router.delete("/{order_id}")
async def delete_order(
    order_id: int, session: AsyncSession = Depends(get_session_to_db)
):
    return await crud.delete_order_crud(order_id=order_id, session=session)


@router.post("/{order_id}/products/{product_id}")
async def add_product_to_order(
    product_id: int, order_id: int, session: AsyncSession = Depends(get_session_to_db)
):
    return await crud.add_product_to_order_crud(
        product_id=product_id, order_id=order_id, session=session
    )


@router.get("/{order_id}/details")
async def get_info_about_order(
    order_id: int, session: AsyncSession = Depends(get_session_to_db)
):
    return await crud.get_info_about_order_crud(order_id=order_id, session=session)
