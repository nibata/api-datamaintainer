"""se agrega campo age para registrar la edad

Revision ID: 6496e7e96b57
Revises: 9e2f15c4baa3
Create Date: 2023-01-14 13:44:47.846346

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6496e7e96b57'
down_revision = '9e2f15c4baa3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('age', sa.Integer(), nullable=True), schema='authentication')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'age', schema='authentication')
    # ### end Alembic commands ###