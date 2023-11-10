from sqlmodel import Field, SQLModel
from datetime import datetime

from ...modules.humps_implementation_module import to_kebab


# BASE
class ProductMovesBase(SQLModel):
    product: str = Field(nullable=False)
    type_movement: str = Field(nullable=False)
    quantity_units: int = Field(nullable=False)
    time_at: datetime = Field(nullable=False, default_factory=datetime.utcnow)

    class Config:
        alias_generator = to_kebab
        allow_population_by_field_name = True


# TABLES
class ProductMoves(ProductMovesBase, table=True):
    """User Class contains standard information for a User."""

    __tablename__ = "product_moves"
    __table_args__ = {"schema": "stock",
                      "extend_existing": True}

    # Fields
    id: int = Field(nullable=False, primary_key=True)


class ProductMovesRead(ProductMoves):
    ...
