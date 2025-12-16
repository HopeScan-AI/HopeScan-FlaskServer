import sqlalchemy as sa
from alembic import op

revision = 'e6315ef8cd88'
down_revision = '61f07d713900'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('payments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('subscription_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_payments_subscription', 'subscription', ['subscription_id'], ['id'])


def downgrade():
    with op.batch_alter_table('payments', schema=None) as batch_op:
        batch_op.drop_constraint('fk_payments_subscription', type_='foreignkey')
        batch_op.drop_column('subscription_id')

