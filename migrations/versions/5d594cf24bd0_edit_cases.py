"""edit cases

Revision ID: 5d594cf24bd0
Revises: 
Create Date: 2025-01-30 21:48:06.617321

"""
import sqlalchemy as sa
from alembic import op

revision = '5d594cf24bd0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('drive_image',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('old_diagnose', sa.String(length=20), nullable=True),
    sa.Column('folder_id', sa.String(length=20), nullable=True),
    sa.Column('folder_name', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('drive_image', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_drive_image_id'), ['id'], unique=False)

    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('role', sa.String(length=10), nullable=True),
    sa.Column('verification_code', sa.String(length=10), nullable=True),
    sa.Column('is_verified', sa.Boolean(), nullable=True),
    sa.Column('provider', sa.String(length=20), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('deleted_by', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('cases',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('create_date', sa.Date(), nullable=False),
    sa.Column('comments', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('deleted_by', sa.Integer(), nullable=True),
    sa.Column('updated_by', sa.Integer(), nullable=True),
    sa.Column('creator_id', sa.Integer(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('cases', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_cases_id'), ['id'], unique=False)

    op.create_table('doctor_diagnose',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('image_drive_id', sa.String(length=50), nullable=False),
    sa.Column('diagnose', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['image_drive_id'], ['drive_image.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('doctor_diagnose', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_doctor_diagnose_id'), ['id'], unique=False)

    op.create_table('health_provider',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('provider_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['provider_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('health_provider', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_health_provider_id'), ['id'], unique=False)

    op.create_table('notifications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('is_read', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('action_url', sa.String(length=255), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('message', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('notifications', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_notifications_id'), ['id'], unique=False)

    op.create_table('images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('file_name', sa.String(length=255), nullable=False),
    sa.Column('file_path', sa.String(length=500), nullable=False),
    sa.Column('diagnose', sa.String(length=500), nullable=True),
    sa.Column('comments', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('case_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['case_id'], ['cases.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('images', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_images_id'), ['id'], unique=False)



def downgrade():
    with op.batch_alter_table('images', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_images_id'))

    op.drop_table('images')
    with op.batch_alter_table('notifications', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_notifications_id'))

    op.drop_table('notifications')
    with op.batch_alter_table('health_provider', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_health_provider_id'))

    op.drop_table('health_provider')
    with op.batch_alter_table('doctor_diagnose', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_doctor_diagnose_id'))

    op.drop_table('doctor_diagnose')
    with op.batch_alter_table('cases', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_cases_id'))

    op.drop_table('cases')

    op.drop_table('users')
    with op.batch_alter_table('drive_image', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_drive_image_id'))

    op.drop_table('drive_image')
