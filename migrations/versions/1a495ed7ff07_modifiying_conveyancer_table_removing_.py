"""modifiying conveyancer table - removing code, changoing lrid to PK and removing title_number

Revision ID: 1a495ed7ff07
Revises: e471a3b5e74
Create Date: 2014-09-15 09:29:43.751434

"""

# revision identifiers, used by Alembic.
revision = '1a495ed7ff07'
down_revision = 'e471a3b5e74'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    op.create_table('conveyancer',
                    sa.Column('lrid', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('address', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('lrid')
    )

    op.create_table('token',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('code', sa.String(), nullable=True),
                    sa.Column('conveyancer_lrid', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('confirmed', sa.DateTime(), nullable=True),
                    sa.Column('title_number', sa.String(), nullable=False),
                    sa.Column('task', sa.String(), nullable=False),
                    sa.Column('client_details', sa.TEXT(), nullable=False),
                    sa.Column('expiry_date', sa.String(), nullable=True),
                    sa.ForeignKeyConstraint(['conveyancer_lrid'], ['conveyancer.lrid'], ),
                    sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('conveyancer')
    op.drop_table('token')
