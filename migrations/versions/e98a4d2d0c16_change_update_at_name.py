"""change update_at name

Revision ID: e98a4d2d0c16
Revises: 470f15432986
Create Date: 2023-09-02 20:31:48.385423

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e98a4d2d0c16'
down_revision = '470f15432986'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(), nullable=True))
        batch_op.drop_column('update_at')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('update_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
        batch_op.drop_column('updated_at')

    # ### end Alembic commands ###