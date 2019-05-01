'''
Initial creation of Short table

Revision ID: 9f6535f6f08e
Revises:
Create Date: 2019-05-01 19:14:06.122994
'''

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.

revision = '9f6535f6f08e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'short',
        sa.Column('prime', sa.Integer(), nullable=False),
        sa.Column('symbol', sa.String(), nullable=False),
        sa.Column('target', sa.String(), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=False),
        sa.Column('created', sa.DateTime(), nullable=False),
        sa.Column('visited', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('prime'),
        sa.UniqueConstraint('symbol')
    )


def downgrade():
    op.drop_table('short')
