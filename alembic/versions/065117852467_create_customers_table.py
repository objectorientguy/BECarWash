"""create customers table

Revision ID: 065117852467
Revises: 
Create Date: 2023-03-19 11:07:48.405934

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '065117852467'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('customers', sa.Column('customer_id', sa.String(), nullable=False),
                    sa.Column('customer_name', sa.String(), nullable=False),
                    sa.Column('customer_contact', sa.BIGINT(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('is_new_customer', sa.Boolean(),
                              server_default='t', default=True, nullable=False),
                    sa.PrimaryKeyConstraint('customer_contact'))

    pass


def downgrade():
    op.drop_table('customers')
    pass
