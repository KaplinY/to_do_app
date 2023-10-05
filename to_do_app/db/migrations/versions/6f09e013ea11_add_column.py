"""add column

Revision ID: 6f09e013ea11
Revises: 92d0521a829f
Create Date: 2023-10-04 14:15:16.192242

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f09e013ea11'
down_revision = '92d0521a829f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('share', sa.BigInteger))


def downgrade() -> None:
    op.drop_column('users', 'share')
