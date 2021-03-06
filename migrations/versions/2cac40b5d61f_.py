"""empty message

Revision ID: 2cac40b5d61f
Revises: 21125cd92fa3
Create Date: 2019-10-08 22:55:16.365221

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2cac40b5d61f'
down_revision = '21125cd92fa3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=20), nullable=True),
    sa.Column('_password', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
