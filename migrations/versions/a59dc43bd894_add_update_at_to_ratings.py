"""add update_at to ratings

Revision ID: a59dc43bd894
Revises: e98a4d2d0c16
Create Date: 2023-09-02 20:42:07.249570

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a59dc43bd894'
down_revision = 'e98a4d2d0c16'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('story_ratings', schema=None) as batch_op:
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('story_ratings', schema=None) as batch_op:
        batch_op.drop_column('updated_at')

    # ### end Alembic commands ###
