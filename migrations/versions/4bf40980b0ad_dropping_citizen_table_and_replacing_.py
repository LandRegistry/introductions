"""dropping citizen table and replacing with a token table that holds all of the transaction information.
Also removing code and task from the conveyancer table

Revision ID: 4bf40980b0ad
Revises: 19bd919a58a7
Create Date: 2014-09-12 12:07:34.137892

"""

# revision identifiers, used by Alembic.
revision = '4bf40980b0ad'
down_revision = '19bd919a58a7'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    op.drop_column('conveyancer', 'task')

    op.drop_table('client')

    op.create_table('token',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('code', sa.String(), nullable=True),
                    sa.Column('conveyancer_lrid', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('confirmed', sa.DateTime(), nullable=True),
                    sa.Column('title_number', sa.String(), nullable=False),
                    sa.Column('task', sa.String(), nullable=False),
                    sa.Column('client_details', sa.TEXT(), nullable=False),
                    sa.Column('expiry_date', sa.String(), nullable=True),
                    sa.ForeignKeyConstraint(['code'], ['conveyancer.code'], ),
                    sa.PrimaryKeyConstraint('id')
    )

    pass


def downgrade():
    op.drop_table('token')

    op.create_table('client',
                    sa.Column('code', sa.String(), nullable=True),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('lrid', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('confirmed', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['code'], ['conveyancer.code'], ),
                    sa.PrimaryKeyConstraint('id')
    )

    op.add_column('conveyancer', sa.Column('task', sa.TEXT(), nullable=False))
    pass
