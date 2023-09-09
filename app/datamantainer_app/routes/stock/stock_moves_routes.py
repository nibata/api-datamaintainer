from ...controller.stock.stock_moves_controller import StockMoveController
from ...models.stock.stock_moves import ProductMovesRead, ProductMoves
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from ...configs.database import get_session
from typing import List


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

