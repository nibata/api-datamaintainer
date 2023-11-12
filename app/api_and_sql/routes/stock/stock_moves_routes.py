from ...controller.stock.stock_moves_controller import StockMoveController
from ...models.stock.stock_moves import ProductMovesRead, ProductMoves
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, Depends, Query
from ...configs.database import get_session
from typing import List, Annotated
from datetime import date


router = APIRouter()


@router.get("/stock", response_model=List[ProductMovesRead], tags=["Stock"])
async def movement_product(product: str = "Product 1", session: AsyncSession = Depends(get_session)):
    async with session.begin():
        stock_move_controller = StockMoveController(session)
        db_stock_product = await stock_move_controller.get_movement_by_product(product=product)

        session.expunge_all()

        return db_stock_product


@router.get("/stock/all", response_model=List[ProductMovesRead], tags=["Stock"])
async def movement_all_product(session: AsyncSession = Depends(get_session)):
    async with session.begin():
        stock_move_controller = StockMoveController(session)
        db_stock_product = await stock_move_controller.get_all_movement()

        session.expunge_all()

        return db_stock_product


@router.get("/stock/{group_id}/q", response_model=List[ProductMovesRead], tags=["Stock"])
async def movement_all_product(date_movement: Annotated[date | None, Query(alias="date-movement")],
                               group_id: str = None,
                               session: AsyncSession = Depends(get_session)):
    async with session.begin():
        stock_move_controller = StockMoveController(session)
        db_stock_product = await stock_move_controller.get_movement_by_product_and_date(product=group_id,
                                                                                        date_movement=date_movement)

        session.expunge_all()

        return db_stock_product

