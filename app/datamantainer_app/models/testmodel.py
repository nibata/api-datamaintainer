from sqlmodel import SQLModel, Field


class TestTable(SQLModel, table=True):
    __tablename__ = "TestTable"
    __table_args__ = {"schema": "test_schema"}

    id: int = Field(nullable=False, primary_key=True)
    name: str = Field(nullable=False, regex="/^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.'-]+$/u")
    description: str


class ReadTestTable(SQLModel):
    name: str


