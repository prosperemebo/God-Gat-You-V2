"""Add unique constraint to likes

Revision ID: 6fff286a9c8c
Revises: 6ad040d11804
Create Date: 2024-07-04 15:58:05.140969

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6fff286a9c8c'
down_revision = '6ad040d11804'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('likes', schema=None) as batch_op:
        batch_op.create_unique_constraint('unique_user_wallpaper_like', ['user_id', 'wallpaper_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('likes', schema=None) as batch_op:
        batch_op.drop_constraint('unique_user_wallpaper_like', type_='unique')

    # ### end Alembic commands ###
