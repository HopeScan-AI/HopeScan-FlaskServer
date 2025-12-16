"""delete subscribtion type and plan

Revision ID: 2174de51bc12
Revises: 4bace48252a9
Create Date: 2025-04-25 12:24:24.679295

"""
import sqlalchemy as sa
from alembic import op

revision = '2174de51bc12'
down_revision = '4bace48252a9'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('subscription_plan')
    op.drop_table('subscription_type')


def downgrade():
    op.create_table('subscription_type',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('type_name', sa.VARCHAR(length=50), nullable=True),
    sa.Column('user_type', sa.VARCHAR(length=50), nullable=True),
    sa.Column('subscription_period', sa.INTEGER(), nullable=True),
    sa.Column('created_at', sa.DATETIME(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('subscription_plan',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('subscription_price', sa.INTEGER(), nullable=False),
    sa.Column('images_count', sa.INTEGER(), nullable=True),
    sa.Column('icon', sa.VARCHAR(), nullable=True),
    sa.Column('image_price', sa.INTEGER(), nullable=False),
    sa.Column('num_of_providers', sa.INTEGER(), nullable=True),
    sa.Column('subscription_type_id', sa.INTEGER(), nullable=False),
    sa.Column('created_at', sa.DATETIME(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('deleted_at', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['subscription_type_id'], ['subscription_type.id'], name='fk_subscription_plan_type_id'),
    sa.PrimaryKeyConstraint('id')
    )
