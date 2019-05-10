'''
create short table

Revision ID: eccf9a0d9f63
Revises:
Create Date: 2019-05-03 21:24:44.166449
'''

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.

revision = 'eccf9a0d9f63'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'short',
        sa.Column('prime', sa.Integer(), nullable=False),
        sa.Column('symbol', sa.String(length=256), nullable=False),
        sa.Column('target', sa.String(length=1024), nullable=False),
        sa.Column('delay', sa.Integer(), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=False),
        sa.Column('visited', sa.Integer(), nullable=False),
        sa.Column('created', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('prime'),
        sa.UniqueConstraint('symbol'),
        mysql_charset='utf8',
        mysql_collate='utf8_bin',
    )


def downgrade():
    op.drop_table('short')
