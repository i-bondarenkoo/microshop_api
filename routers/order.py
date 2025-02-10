from fastapi import APIRouter, Depends
import crud
from schemas.order import CreateOrderSchema
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db_session

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.post("/")
async def create_order(
    order: CreateOrderSchema, session: AsyncSession = Depends(get_db_session)
):
    return await crud.create_order_crud(order=order, session=session)


@router.get("/")
async def get_all_orders(session: AsyncSession = Depends(get_db_session)):
    return await crud.get_all_orders_crud(session=session)


@router.get("/{order_id}")
async def get_order_by_id(
    order_id: int, session: AsyncSession = Depends(get_db_session)
):
    return await crud.get_order_by_id_crud(order_id=order_id, session=session)


@router.delete("/{order_id}")
async def delete_order(
    order_id: int, session: AsyncSession = Depends(get_db_session)
):
    return await crud.delete_order_crud(order_id=order_id, session=session)
