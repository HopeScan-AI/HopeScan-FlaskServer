"""create plan table

Revision ID: 5338b691a9ce
Revises: c1801a4d29f5
Create Date: 2025-04-19 16:35:23.969190

"""
import sqlalchemy as sa
from alembic import op

revision = '5338b691a9ce'
down_revision = 'c1801a4d29f5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('plans',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('num_of_providers', sa.Integer(), nullable=True),
    sa.Column('icon', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('plan_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('period', sa.Integer(), nullable=True),
    sa.Column('price', sa.Double(), nullable=True),
    sa.Column('plan_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['plan_id'], ['plans.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('plan_type')
    op.drop_table('plans')
