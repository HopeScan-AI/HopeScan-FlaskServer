"""plan edit

Revision ID: 295c4ddb15a9
Revises: 5338b691a9ce
Create Date: 2025-04-23 16:18:11.992186

"""
import sqlalchemy as sa
from alembic import op

revision = '295c4ddb15a9'
down_revision = '5338b691a9ce'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('plan_type', schema=None) as batch_op:
        batch_op.add_column(sa.Column('images_count', sa.Integer(), nullable=True))

    with op.batch_alter_table('plans', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name_arabic', sa.String(length=50), nullable=True))



def downgrade():
    with op.batch_alter_table('plans', schema=None) as batch_op:
        batch_op.drop_column('name_arabic')

    with op.batch_alter_table('plan_type', schema=None) as batch_op:
        batch_op.drop_column('images_count')

