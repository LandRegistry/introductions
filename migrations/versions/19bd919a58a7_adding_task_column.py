"""Adding task column

Revision ID: 19bd919a58a7
Revises: 34768175f672
Create Date: 2014-09-11 10:57:38.396946

"""

# revision identifiers, used by Alembic.
revision = '19bd919a58a7'
down_revision = '34768175f672'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('conveyancer', sa.Column('task', sa.TEXT(), nullable=False))


def downgrade():
    op.drop_column('conveyancer', 'task')
