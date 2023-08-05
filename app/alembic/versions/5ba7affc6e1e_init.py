"""init

Revision ID: 5ba7affc6e1e
Revises: 
Create Date: 2023-08-04 17:42:46.485800

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '5ba7affc6e1e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("CREATE SCHEMA IF NOT EXISTS test_schema")
    table_test = op.create_table('TestTable',
                                 sa.Column('id', sa.Integer(), nullable=False),
                                  sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                                  sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                                  sa.PrimaryKeyConstraint('id'),
                                  schema='test_schema')
    # ### end Alembic commands ###
    test_insert = [{"name": "Nicolás", "description": "TEST"}]

    op.bulk_insert(table_test,
                   test_insert)


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('TestTable', schema='test_schema')
    op.execute("DROP SCHEMA IF EXISTS test_schema")
    # ### end Alembic commands ###
