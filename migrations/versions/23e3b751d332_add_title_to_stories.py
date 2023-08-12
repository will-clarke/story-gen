"""add title to stories

Revision ID: 23e3b751d332
Revises: d18ff610cdd7
Create Date: 2023-08-12 16:23:55.084928

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '23e3b751d332'
down_revision: Union[str, None] = 'd18ff610cdd7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stories', sa.Column('title', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('stories', 'title')
    # ### end Alembic commands ###
