"""payments and subscriptions

Revision ID: 603bfbf87563
Revises: 5d594cf24bd0
Create Date: 2025-03-29 16:17:24.965743

"""
import sqlalchemy as sa
from alembic import op

revision = '603bfbf87563'
down_revision = '5d594cf24bd0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('subscription_plan',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subscription_price', sa.Integer(), nullable=False),
    sa.Column('images_count', sa.Integer(), nullable=True),
    sa.Column('image_price', sa.Integer(), nullable=False),
    sa.Column('num_of_providers', sa.Integer(), nullable=True),
    sa.Column('subscription_type', sa.String(length=50), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('verification_code', sa.String(length=255), nullable=False),
    sa.Column('subscription_plan_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['subscription_plan_id'], ['subscription_plan.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('payments', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_payments_id'), ['id'], unique=False)

    op.create_table('subscription',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('authorization_code', sa.String(length=255), nullable=False),
    sa.Column('subscription_plan_id', sa.String(length=100), nullable=False),
    sa.Column('currency', sa.String(length=10), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('next_billing_date', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['subscription_plan_id'], ['subscription_plan.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('cases', schema=None) as batch_op:
        batch_op.drop_column('created_by')
        batch_op.drop_column('deleted_by')
        batch_op.drop_column('updated_by')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_users_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_users_id'), ['id'], unique=False)



def downgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_id'))
        batch_op.drop_index(batch_op.f('ix_users_email'))

    with op.batch_alter_table('cases', schema=None) as batch_op:
        batch_op.add_column(sa.Column('updated_by', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('deleted_by', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('created_by', sa.INTEGER(), nullable=True))

    op.drop_table('subscription')
    with op.batch_alter_table('payments', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_payments_id'))

    op.drop_table('payments')
    op.drop_table('subscription_plan')
