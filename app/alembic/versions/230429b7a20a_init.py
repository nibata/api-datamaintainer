"""init

Revision ID: 230429b7a20a
Revises: 
Create Date: 2023-08-05 12:15:04.687766

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
from datamantainer_app.models import Password
from datamantainer_app.configs.settings import USER_ADMIN, PASS_ADMIN, ADMIN_EMAIL


# revision identifiers, used by Alembic.
revision = '230429b7a20a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('CREATE SCHEMA IF NOT EXISTS "Authentication"')
    table_group = op.create_table('Group',
                                  sa.Column('Code', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                                  sa.Column('Description', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                                  sa.Column('Id', sa.Integer(), nullable=False),
                                  sa.PrimaryKeyConstraint('Id'),
                                  sa.UniqueConstraint('Code'),
                                  schema='Authentication')

    table_user = op.create_table('User',
                                 sa.Column('FullName', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                                 sa.Column('Email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                                 sa.Column('IsActive', sa.Boolean(), nullable=False),
                                 sa.Column('Id', sa.Integer(), nullable=False),
                                 sa.PrimaryKeyConstraint('Id'),
                                 schema='Authentication')

    table_passwors = op.create_table('Password',
                                     sa.Column('CreationDate', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                                     sa.Column('IsActive', sa.Boolean(), nullable=False),
                                     sa.Column('ExpirationDate', sa.Date(), nullable=True),
                                     sa.Column('Id', sa.Integer(), nullable=False),
                                     sa.Column('UserId', sa.Integer(), nullable=False),
                                     sa.Column('HashedPassword', sqlmodel.sql.sqltypes.AutoString(length=120), nullable=False),
                                     sa.ForeignKeyConstraint(['UserId'], ['Authentication.User.Id'], ),
                                     sa.PrimaryKeyConstraint('Id'),
                                     schema='Authentication')

    table_relation_user_groups = op.create_table('UserGroupLink',
                                                 sa.Column('UserId', sa.Integer(), nullable=False),
                                                 sa.Column('GroupId', sa.Integer(), nullable=False),
                                                 sa.ForeignKeyConstraint(['GroupId'], ['Authentication.Group.Id'], ),
                                                 sa.ForeignKeyConstraint(['UserId'], ['Authentication.User.Id'], ),
                                                 sa.PrimaryKeyConstraint('UserId', 'GroupId'),
                                                 schema='Authentication')
    # ### end Alembic commands ###
    # DEFAULT DATA
    roles = [{"Code": "ADMINISTRATOR", "Description": "Administrator privileges role"},
             {"Code": "SELECT", "Description": "Basic select role"},
             {"Code": "INSERT", "Description": "Basic insert role"},
             {"Code": "DEFAULT", "Description": "Default role"}]

    user = [{"Email": ADMIN_EMAIL, "FullName": USER_ADMIN, "IsActive": True}]

    op.bulk_insert(table_group, roles)
    op.bulk_insert(table_user, user)
    op.execute(f"""
                INSERT INTO "Authentication"."UserGroupLink"("UserId", "GroupId")
                VALUES ((SELECT "Id" FROM "Authentication"."User" WHERE "Email"='{ADMIN_EMAIL}'),
                        (SELECT "Id" FROM "Authentication"."Group" WHERE "Code"='ADMINISTRATOR')),
                        
                        ((SELECT "Id" FROM "Authentication"."User" WHERE "Email"='{ADMIN_EMAIL}'),
                        (SELECT "Id" FROM "Authentication"."Group" WHERE "Code"='SELECT')),
                        
                        ((SELECT "Id" FROM "Authentication"."User" WHERE "Email"='{ADMIN_EMAIL}'),
                        (SELECT "Id" FROM "Authentication"."Group" WHERE "Code"='INSERT')),
                        
                        ((SELECT "Id" FROM "Authentication"."User" WHERE "Email"='{ADMIN_EMAIL}'),
                        (SELECT "Id" FROM "Authentication"."Group" WHERE "Code"='DEFAULT'))
                        """)

    hashed_password = Password.set_password(PASS_ADMIN)

    op.execute(f"""
                INSERT INTO "Authentication"."Password" ("UserId", "IsActive", "HashedPassword")
                VALUES ((SELECT "Id" FROM "Authentication"."User" WHERE "Email"='{ADMIN_EMAIL}'),
                        true,
                        '{hashed_password}')
                """)


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('UserGroupLink', schema='Authentication')
    op.drop_table('Password', schema='Authentication')
    op.drop_table('User', schema='Authentication')
    op.drop_table('Group', schema='Authentication')
    op.execute('DROP SCHEMA IF EXISTS "Authentication"')
    # ### end Alembic commands ###
