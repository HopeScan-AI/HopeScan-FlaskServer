"""subscription type edit

Revision ID: 7318e193acc0
Revises: d2d5e617c0b2
Create Date: 2025-03-31 10:50:06.851915

"""
import sqlalchemy as sa
from alembic import op

revision = '7318e193acc0'
down_revision = 'd2d5e617c0b2'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('subscription_type', schema=None) as batch_op:
        batch_op.add_column(sa.Column('subscription_period', sa.Integer(), nullable=True))



def downgrade():
    with op.batch_alter_table('subscription_type', schema=None) as batch_op:
        batch_op.drop_column('subscription_period')

