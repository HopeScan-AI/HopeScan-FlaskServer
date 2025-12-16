"""add image cost to plan

Revision ID: 61f07d713900
Revises: 2174de51bc12
Create Date: 2025-04-25 12:47:43.884200

"""
import sqlalchemy as sa
from alembic import op

revision = '61f07d713900'
down_revision = '2174de51bc12'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('payments', schema=None) as batch_op:
        batch_op.drop_constraint('fk_payments_plans_id', type_='foreignkey')
        batch_op.drop_column('plans_id')

    with op.batch_alter_table('plans', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_cost', sa.Double(), nullable=True))

    with op.batch_alter_table('subscription', schema=None) as batch_op:
        batch_op.add_column(sa.Column('plan_type_id', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('images_count', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('num_of_providers', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('image_cost', sa.Double(), nullable=True))
        batch_op.create_foreign_key('fk_subscription_plan_type_id', 'plan_type', ['plan_type_id'], ['id'])


def downgrade():
    with op.batch_alter_table('subscription', schema=None) as batch_op:
        batch_op.drop_constraint('fk_subscription_plan_type_id', type_='foreignkey')
        batch_op.drop_column('image_cost')
        batch_op.drop_column('num_of_providers')
        batch_op.drop_column('images_count')
        batch_op.drop_column('plan_type_id')

    with op.batch_alter_table('plans', schema=None) as batch_op:
        batch_op.drop_column('image_cost')

    with op.batch_alter_table('payments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('plans_id', sa.INTEGER(), nullable=False))
        batch_op.create_foreign_key('fk_payments_plans_id', 'plans', ['plans_id'], ['id'])
