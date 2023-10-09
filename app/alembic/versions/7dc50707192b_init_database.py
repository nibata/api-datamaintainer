"""init database

Revision ID: 7dc50707192b
Revises: 
Create Date: 2023-10-08 21:11:17.048332

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
from faker import Faker
from faker.providers import DynamicProvider
from datetime import datetime
from datamantainer_app.models import Password
from datamantainer_app.configs.settings import USER_ADMIN, PASS_ADMIN, ADMIN_EMAIL

product_provider = DynamicProvider(provider_name="product", elements=["Product 1", "Product 2", "Product 3"])
movement_type_provider = DynamicProvider(provider_name="movement_type", elements=["Sell", "Buy"])

fake = Faker()
fake.add_provider(product_provider)
fake.add_provider(movement_type_provider)

# revision identifiers, used by Alembic.
revision = '7dc50707192b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('CREATE SCHEMA IF NOT EXISTS "stock"')
    op.execute('CREATE SCHEMA IF NOT EXISTS "authentication"')

    table_group = op.create_table('group',
                                  sa.Column('code', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                                  sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
                                  sa.Column('id', sa.Integer(), nullable=False),
                                  sa.PrimaryKeyConstraint('id'),
                                  sa.UniqueConstraint('code'),
                                  schema='authentication')

    table_user = op.create_table('user',
                                 sa.Column('full_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                                 sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                                 sa.Column('id', sa.Integer(), nullable=False),
                                 sa.Column('is_active', sa.Boolean(), server_default=sa.text('false'), nullable=False),
                                 sa.PrimaryKeyConstraint('id'),
                                 schema='authentication')

    table_produc_moves = op.create_table('product_moves',
                                         sa.Column('product', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                                         sa.Column('type_movement', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                                         sa.Column('quantity_units', sa.Integer(), nullable=False),
                                         sa.Column('time_at', sa.DateTime(), nullable=False),
                                         sa.Column('id', sa.Integer(), nullable=False),
                                         sa.PrimaryKeyConstraint('id'),
                                         schema='stock')

    table_passwors = op.create_table('password',
                                     sa.Column('creation_date', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                                     sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False),
                                     sa.Column('expiration_date', sa.Date(), nullable=True),
                                     sa.Column('id', sa.Integer(), nullable=False),
                                     sa.Column('user_id', sa.Integer(), nullable=False),
                                     sa.Column('hashed_password', sqlmodel.sql.sqltypes.AutoString(length=120), nullable=False),
                                     sa.ForeignKeyConstraint(['user_id'], ['authentication.user.id'], ),
                                     sa.PrimaryKeyConstraint('id'),
                                     schema='authentication')

    table_relation_user_groups = op.create_table('user_group_link',
                                                 sa.Column('user_id', sa.Integer(), nullable=False),
                                                 sa.Column('group_id', sa.Integer(), nullable=False),
                                                 sa.ForeignKeyConstraint(['group_id'], ['authentication.group.id'], ),
                                                 sa.ForeignKeyConstraint(['user_id'], ['authentication.user.id'], ),
                                                 sa.PrimaryKeyConstraint('user_id', 'group_id'),
                                                 schema='authentication')
    # ### end Alembic commands ###

    data = []
    for i in range(0, 10000):
        data.append({"product": fake.product(),
                     "type_movement": fake.movement_type(),
                     "quantity_units": fake.pyint(min_value=1, max_value=15),
                     "time_at": fake.date_time_between(start_date=datetime(2000, 1, 1, 0, 0, 0),
                                                       end_date=datetime(2024, 1, 1, 0, 0, 0))
                     })

    op.bulk_insert(table_produc_moves, data)

    roles = [{"code": "ADMINISTRATOR", "description": "Administrator privileges role"},
             {"code": "SELECT", "description": "Basic select role"},
             {"code": "INSERT", "description": "Basic insert role"},
             {"code": "DEFAULT", "description": "Default role"}]

    user = [{"email": ADMIN_EMAIL, "full_name": USER_ADMIN, "is_active": True}]

    op.bulk_insert(table_group, roles)
    op.bulk_insert(table_user, user)
    op.execute(f"""
                    INSERT INTO "authentication"."user_group_link"("user_id", "group_id")
                    VALUES ((SELECT "id" FROM "authentication"."user" WHERE "email"='{ADMIN_EMAIL}'),
                            (SELECT "id" FROM "authentication"."group" WHERE "code"='ADMINISTRATOR')),

                            ((SELECT "id" FROM "authentication"."user" WHERE "email"='{ADMIN_EMAIL}'),
                            (SELECT "id" FROM "authentication"."group" WHERE "code"='SELECT')),

                            ((SELECT "id" FROM "authentication"."user" WHERE "email"='{ADMIN_EMAIL}'),
                            (SELECT "id" FROM "authentication"."group" WHERE "code"='INSERT')),

                            ((SELECT "id" FROM "authentication"."user" WHERE "email"='{ADMIN_EMAIL}'),
                            (SELECT "id" FROM "authentication"."group" WHERE "code"='DEFAULT'))
                            """)

    hashed_password = Password.set_password(PASS_ADMIN)

    op.execute(f"""
                    INSERT INTO "authentication"."password" ("user_id", "is_active", "hashed_password")
                    VALUES ((SELECT "id" FROM "authentication"."user" WHERE "email"='{ADMIN_EMAIL}'),
                            true,
                            '{hashed_password}')
                    """)


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_group_link', schema='authentication')
    op.drop_table('password', schema='authentication')
    op.drop_table('product_moves', schema='stock')
    op.drop_table('user', schema='authentication')
    op.drop_table('group', schema='authentication')

    op.execute('DROP SCHEMA IF EXISTS "stock"')
    op.execute('DROP SCHEMA IF EXISTS "authentication"')
    # ### end Alembic commands ###