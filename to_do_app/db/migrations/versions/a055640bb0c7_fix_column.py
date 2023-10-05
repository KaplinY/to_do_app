"""fix column

Revision ID: a055640bb0c7
Revises: 9c64cf644dd5
Create Date: 2023-10-04 14:40:33.843540

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a055640bb0c7'
down_revision = '9c64cf644dd5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column('users', 'share')
    op.add_column('users', sa.Column('share', sa.BigInteger, nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'share')
