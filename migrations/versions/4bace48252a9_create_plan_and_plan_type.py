"""create plan and plan_type

Revision ID: 4bace48252a9
Revises: 295c4ddb15a9
Create Date: 2025-04-25 12:15:27.023263
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4bace48252a9'
down_revision = '295c4ddb15a9'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('payments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('plans_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key('fk_payments_plans_id', 'plans', ['plans_id'], ['id'])
        batch_op.drop_column('subscription_plan_id')

    with op.batch_alter_table('subscription', schema=None) as batch_op:
        batch_op.add_column(sa.Column('plans_id', sa.String(length=100), nullable=False))
        batch_op.create_foreign_key('fk_subscription_plans_id', 'plans', ['plans_id'], ['id'])
        batch_op.drop_column('subscription_plan_id')

    # with op.batch_alter_table('subscription_plan', schema=None) as batch_op:
        # batch_op.add_column(sa.Column('subscription_price', sa.Integer(), nullable=False))
        # batch_op.add_column(sa.Column('images_count', sa.Integer(), nullable=True))
        # batch_op.add_column(sa.Column('icon', sa.String(), nullable=True))
    
    # with op.batch_alter_table('subscription_plan', schema=None) as batch_op:
        # batch_op.add_column(sa.Column('image_price', sa.Integer(), nullable=False))
        # batch_op.add_column(sa.Column('num_of_providers', sa.Integer(), nullable=True))
    
    # op.add_column('subscription_plan', sa.Column('subscription_type_id', sa.Integer(), nullable=False))
    
    # op.add_column('subscription_plan', sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False))
    
    op.add_column('subscription_plan', sa.Column( 'deleted_at', sa.DateTime(), nullable=True))

    with op.batch_alter_table('subscription_plan', schema=None) as batch_op:
        batch_op.alter_column('id', existing_type=sa.INTEGER(), nullable=False, autoincrement=True)
        
    with op.batch_alter_table('subscription_plan', schema=None) as batch_op:
        batch_op.create_foreign_key('fk_subscription_plan_type_id', 'subscription_type', ['subscription_type_id'], ['id'])

    with op.batch_alter_table('subscription_type', schema=None) as batch_op:
        # batch_op.add_column(sa.Column('type_name', sa.String(length=50), nullable=True))
        # batch_op.add_column(sa.Column('user_type', sa.String(length=50), nullable=True))
        # batch_op.add_column(sa.Column('subscription_period', sa.Integer(), nullable=True))
        # batch_op.add_column(sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False))
        batch_op.alter_column('id', existing_type=sa.INTEGER(), nullable=False, autoincrement=True)


def downgrade():
    with op.batch_alter_table('subscription_type', schema=None) as batch_op:
        batch_op.alter_column('id', existing_type=sa.INTEGER(), nullable=True, autoincrement=True)
        batch_op.drop_column('created_at')
        batch_op.drop_column('subscription_period')
        batch_op.drop_column('user_type')
        batch_op.drop_column('type_name')

    with op.batch_alter_table('subscription_plan', schema=None) as batch_op:
        batch_op.drop_constraint('fk_subscription_plan_type_id', type_='foreignkey')
    with op.batch_alter_table('subscription_plan', schema=None) as batch_op:
        batch_op.alter_column('id', existing_type=sa.INTEGER(), nullable=True, autoincrement=True)
    with op.batch_alter_table('subscription_plan', schema=None) as batch_op:
        batch_op.drop_column('deleted_at')
    with op.batch_alter_table('subscription_plan', schema=None) as batch_op:
        batch_op.drop_column('created_at')
    with op.batch_alter_table('subscription_plan', schema=None) as batch_op:
        batch_op.drop_column('subscription_type_id')
        # batch_op.drop_column('num_of_providers')
        # batch_op.drop_column('image_price')
        # batch_op.drop_column('icon')
        # batch_op.drop_column('images_count')
        # batch_op.drop_column('subscription_price')

    with op.batch_alter_table('subscription', schema=None) as batch_op:
        batch_op.add_column(sa.Column('subscription_plan_id', sa.VARCHAR(length=100), nullable=False))
        batch_op.drop_constraint('fk_subscription_plans_id', type_='foreignkey')
        batch_op.create_foreign_key('fk_subscription_subscription_plan_id', 'subscription_plan', ['subscription_plan_id'], ['id'])
        batch_op.drop_column('plans_id')

    with op.batch_alter_table('payments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('subscription_plan_id', sa.INTEGER(), nullable=False))
        batch_op.drop_constraint('fk_payments_plans_id', type_='foreignkey')
        batch_op.create_foreign_key('fk_payments_subscription_plan_id', 'subscription_plan', ['subscription_plan_id'], ['id'])
        batch_op.drop_column('plans_id')
