from sqlmodel.ext.asyncio.session import AsyncSession
from ...models.stock import stock_moves
from datetime import date, timedelta
from sqlmodel import select


class StockMoveController:
    """
    It defines the possible actions to take when stocks refers like get the moves of certain product or
    any possible combination.
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_movement_by_product_and_date(self, product: str, date_movement: date):
        rtn = await self.session.execute(select(stock_moves.ProductMoves)
                                         .where(stock_moves.ProductMoves.product == product,
                                                stock_moves.ProductMoves.time_at >= date_movement,
                                                stock_moves.ProductMoves.time_at < (date_movement + timedelta(days=1))))
        return rtn.scalars().all()

    async def get_movement_by_product(self, product: str):
        rtn = await self.session.execute(select(stock_moves.ProductMoves)
                                         .where(stock_moves.ProductMoves.product == product))
        return rtn.scalars().all()

    async def get_all_movement(self):
        rtn = await self.session.execute(select(stock_moves.ProductMoves))
        return rtn.scalars().all()

