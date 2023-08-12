"""create story table

Revision ID: 0fbb19568c7a
Revises: 
Create Date: 2023-08-12 12:17:23.577573

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = '0fbb19568c7a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'story',
        sa.Column('id',UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('story', sa.String),
        sa.Column('prompt',sa.String),
        sa.Column('expected_length',sa.Integer),
        sa.Column('model_name', sa.String),
        sa.Column('updated_at',sa.DateTime, default=datetime.datetime.utcnow),
        sa.Column('created_at',sa.DateTime, default=datetime.datetime.utcnow),
    )


def downgrade() -> None:
    op.drop_table('story')
