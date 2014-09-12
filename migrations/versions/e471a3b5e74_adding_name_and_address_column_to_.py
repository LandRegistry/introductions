"""adding name and address column to conveyancer

Revision ID: e471a3b5e74
Revises: 4bf40980b0ad
Create Date: 2014-09-12 13:40:49.953943

"""

# revision identifiers, used by Alembic.
revision = 'e471a3b5e74'
down_revision = '4bf40980b0ad'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('conveyancer', sa.Column('name', sa.String(), nullable=False))
    op.add_column('conveyancer', sa.Column('address', sa.String(), nullable=False))


def downgrade():
    op.drop_column('conveyancer', 'name')
    op.drop_column('conveyancer', 'address')
