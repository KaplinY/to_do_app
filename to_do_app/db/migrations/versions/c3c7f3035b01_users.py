"""users

Revision ID: c3c7f3035b01
Revises: 
Create Date: 2023-10-01 23:27:43.210141

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3c7f3035b01'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
    sa.Column('user_id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.Column('password', sa.Text(), nullable=False),
    sa.Column('email', sa.Text(), nullable = False),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('username')
    )


def downgrade() -> None:
    op.drop_table('users')
