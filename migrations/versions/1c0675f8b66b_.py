"""empty message

Revision ID: 1c0675f8b66b
Revises: 23e3b751d332
Create Date: 2023-08-12 20:18:07.327589

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1c0675f8b66b'
down_revision: Union[str, None] = '23e3b751d332'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
