"""rename code column to token

Revision ID: b851d7566c3
Create Date: 2014-09-17 08:29:00.138766

"""

# revision identifiers, used by Alembic.
revision = 'b851d7566c3'

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

    op.create_table('relationship',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('token', sa.String(), nullable=True),
                    sa.Column('conveyancer_lrid', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('client_lrid', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('confirmed', sa.DateTime(), nullable=True),
                    sa.Column('title_number', sa.String(), nullable=False),
                    sa.Column('task', sa.String(), nullable=False),
                    sa.Column('expiry_date', sa.String(), nullable=True),
                    sa.ForeignKeyConstraint(['conveyancer_lrid'], ['conveyancer.lrid'], ),
                    sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('conveyancer')
    op.drop_table('relationship')
