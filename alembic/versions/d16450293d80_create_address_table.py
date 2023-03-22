"""create address table

Revision ID: d16450293d80
Revises: ead0be0da6df
Create Date: 2023-03-21 09:29:03.671999

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd16450293d80'
down_revision = 'ead0be0da6df'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint(None, 'customers', ['customer_contact'])
    op.create_table('address',
                    sa.Column('address_id', sa.BIGINT(),
                              nullable=False, primary_key=True),
                    sa.Column('user_contact', sa.BIGINT(),
                              nullable=False),
                    sa.Column('address_title', sa.String(),
                              nullable=False),
                    sa.Column('address_name', sa.String(), nullable=False),
                    sa.Column('city', sa.String(), nullable=False),
                    sa.Column('pincode', sa.BIGINT(),
                              nullable=False,)
                    )
    op.create_foreign_key('address_user_fk', source_table="address", referent_table="customers", local_cols=[
                          'user_contact'], remote_cols=['customer_contact'], ondelete="CASCADE")

    pass


def downgrade():
    op.drop_table('address')
    pass
