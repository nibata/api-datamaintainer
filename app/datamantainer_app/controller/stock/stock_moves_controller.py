from sqlmodel.ext.asyncio.session import AsyncSession
from ...models.stock import stock_moves
from sqlmodel import select
from datetime import date


class StockMoveController:
    """
    It defines the possible actions to take when stocks refers like get the moves of certain product or
    any possible combination.
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_movement_by_product_and_date(self, product: str, date_movement: date):
        rtn = await self.session.execute(select(stock_moves.ProductMoves)
                                         .where(stock_moves.ProductMoves.Product == product,
                                                stock_moves.ProductMoves.TimeAt == date_movement))
        return rtn.scalars().all()

    async def get_movement_by_product(self, product: str):
        rtn = await self.session.execute(select(stock_moves.ProductMoves)
                                         .where(stock_moves.ProductMoves.Product == product))
        return rtn.scalars().all()

    async def get_all_movement(self):
        rtn = await self.session.execute(select(stock_moves.ProductMoves))
        return rtn.scalars().all()

