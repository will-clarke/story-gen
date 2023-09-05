"""Alter DataReddit - add top_comment field

Revision ID: 493bf6006a67
Revises: 717ae8112a61
Create Date: 2023-09-05 21:20:38.415545

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '493bf6006a67'
down_revision = '717ae8112a61'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('data_reddit', schema=None) as batch_op:
        batch_op.add_column(sa.Column('top_comment', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('data_reddit', schema=None) as batch_op:
        batch_op.drop_column('top_comment')

    # ### end Alembic commands ###
