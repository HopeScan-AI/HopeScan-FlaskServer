"""edit payment

Revision ID: 22b9117b306c
Revises: e6315ef8cd88
Create Date: 2025-04-25 13:18:48.387264

"""
import sqlalchemy as sa
from alembic import op

revision = '22b9117b306c'
down_revision = 'e6315ef8cd88'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('payments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.String(length=50), nullable=True))



def downgrade():
    with op.batch_alter_table('payments', schema=None) as batch_op:
        batch_op.drop_column('status')

