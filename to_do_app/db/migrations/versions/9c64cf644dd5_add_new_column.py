"""Add new column

Revision ID: 9c64cf644dd5
Revises: 6f09e013ea11
Create Date: 2023-10-04 14:21:18.312892

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c64cf644dd5'
down_revision = '6f09e013ea11'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('share', sa.BigInteger))
    op.drop_column('todo', 'share')


def downgrade() -> None:
    op.drop_column('users', 'share')
