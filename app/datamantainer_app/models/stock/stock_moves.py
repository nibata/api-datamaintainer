from sqlmodel import Field, SQLModel
from datetime import datetime


# BASE
class ProductMovesBase(SQLModel):
    product: str = Field(nullable=False)
    type_movement: str = Field(nullable=False)
    quantity_units: int = Field(nullable=False)
    time_at: datetime = Field(nullable=False, default_factory=datetime.utcnow)


# TABLES
class ProductMoves(ProductMovesBase, table=True):
    """User Class contains standard information for a User."""

    __tablename__ = "product_moves"
    __table_args__ = {"schema": "stock"}

    # Fields
    id: int = Field(nullable=False, primary_key=True)


class ProductMovesRead(ProductMoves):
    ...
