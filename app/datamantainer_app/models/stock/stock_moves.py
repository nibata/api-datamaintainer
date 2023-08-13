from sqlmodel import Field, SQLModel
from datetime import datetime


# BASE
class ProductMovesBase(SQLModel):
    Product: str = Field(nullable=False)
    TypeMovement: str = Field(nullable=False)
    QuantityUnits: int = Field(nullable=False)
    TimeAt: datetime = Field(nullable=False, default_factory=datetime.utcnow)


# TABLES
class ProductMoves(ProductMovesBase, table=True):
    """User Class contains standard information for a User."""

    __tablename__ = "ProductMoves"
    __table_args__ = {"schema": "Stock"}

    # Fields
    Id: int = Field(nullable=False, primary_key=True)


class ProductMovesRead(ProductMoves):
    ...
