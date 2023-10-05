"""todo

Revision ID: 92d0521a829f
Revises: c3c7f3035b01
Create Date: 2023-10-02 20:41:08.246055

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "92d0521a829f"
down_revision = "c3c7f3035b01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('todo',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('day', sa.Text(), nullable=False),
    sa.Column('task', sa.Text(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('todo')
