"""create bookings table

Revision ID: 6856ffa10526
Revises: d16450293d80
Create Date: 2023-03-21 17:13:36.908474

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6856ffa10526'
down_revision = 'd16450293d80'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint(None, 'address', ['address_id'])
    op.create_table('bookings',
                    sa.Column('booking_id', sa.BIGINT(),
                              nullable=False, primary_key=True),
                    sa.Column('user_contact', sa.BIGINT(), nullable=False),
                    sa.Column('address_id', sa.BIGINT(), nullable=False),
                    sa.Column('booking_time', sa.String(), nullable=False),
                    sa.Column('booking_date', sa.String(), nullable=False),
                    sa.Column('services', sa.String(), nullable=False),
                    sa.Column('final_amount', sa.String(), nullable=False),
                    sa.Column('payment_mode', sa.String(), nullable=False),
                    )
    op.create_foreign_key('booking_user_fk', source_table="bookings", referent_table="customers", local_cols=[
                          'user_contact'], remote_cols=['customer_contact'], ondelete="CASCADE")
    op.create_foreign_key('booking_address_fk', source_table="bookings", referent_table="address", local_cols=[
                          'address_id'], remote_cols=['address_id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_table('bookings')
    pass
