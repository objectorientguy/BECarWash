"""create customer table

Revision ID: ead0be0da6df
Revises: 
Create Date: 2023-03-21 08:37:18.495336

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ead0be0da6df'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('customers',
                    sa.Column('customer_id', sa.String(),
                              nullable=False),
                    sa.Column('customer_name', sa.String(),
                              nullable=False, primary_key=True),
                    sa.Column('customer_contact', sa.BIGINT(), nullable=False),
                    sa.Column('is_new_customer', sa.Boolean(),
                              server_default='t', nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.UniqueConstraint('customer_id')
                    )
    pass


def downgrade():
    op.drop_table('customers')
    pass
