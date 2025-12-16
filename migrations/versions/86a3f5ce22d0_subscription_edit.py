"""subscription edit

Revision ID: 86a3f5ce22d0
Revises: 7318e193acc0
Create Date: 2025-04-01 13:49:16.599132

"""
import sqlalchemy as sa
from alembic import op

revision = '86a3f5ce22d0'
down_revision = '7318e193acc0'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('subscription', schema=None) as batch_op:
        batch_op.add_column(sa.Column('used_images', sa.Integer(), nullable=True))



def downgrade():
    with op.batch_alter_table('subscription', schema=None) as batch_op:
        batch_op.drop_column('used_images')

