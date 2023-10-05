"""shared add

Revision ID: b27858b3a817
Revises: a055640bb0c7
Create Date: 2023-10-04 22:49:37.983952

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b27858b3a817'
down_revision = 'a055640bb0c7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('shared',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('friends_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('shared')
