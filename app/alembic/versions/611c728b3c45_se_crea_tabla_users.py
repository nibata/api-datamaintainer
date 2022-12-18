"""se crea tabla Users

Revision ID: 611c728b3c45
Revises: 
Create Date: 2022-12-18 16:06:35.500944

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '611c728b3c45'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("CREATE SCHEMA IF NOT EXISTS authentication")
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='authentication'
    )
    op.create_index(op.f('ix_authentication_users_email'), 'users', ['email'], unique=True, schema='authentication')
    op.create_index(op.f('ix_authentication_users_id'), 'users', ['id'], unique=False, schema='authentication')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_authentication_users_id'), table_name='users', schema='authentication')
    op.drop_index(op.f('ix_authentication_users_email'), table_name='users', schema='authentication')
    op.drop_table('users', schema='authentication')
    # ### end Alembic commands ###
