'''
empty message

Revision ID: 0c4564403d6d
Revises: 9f6535f6f08e
Create Date: 2019-05-03 20:10:40.841419
'''

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.

revision = '0c4564403d6d'
down_revision = '9f6535f6f08e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'short', sa.Column('delay', sa.Integer(), nullable=False)
    )


def downgrade():
    op.drop_column('short', 'delay')
