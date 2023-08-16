"""empty message

Revision ID: d4111644c89c
Revises: 66ac74128936
Create Date: 2023-08-15 20:36:19.343254

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4111644c89c'
down_revision = '66ac74128936'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stories',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('prompt', sa.String(), nullable=True),
    sa.Column('length', sa.Integer(), nullable=True),
    sa.Column('model_name', sa.String(), nullable=True),
    sa.Column('update_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('story_categories',
    sa.Column('story_id', sa.UUID(), nullable=False),
    sa.Column('category_type', sa.String(), nullable=False),
    sa.Column('category', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['story_id'], ['stories.id'], ),
    sa.PrimaryKeyConstraint('story_id', 'category_type', 'category')
    )
    op.create_table('story_ratings',
    sa.Column('story_id', sa.UUID(), nullable=False),
    sa.Column('rating_type', sa.String(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('prompt', sa.String(), nullable=True),
    sa.Column('model_name', sa.String(), nullable=True),
    sa.Column('model_output', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['story_id'], ['stories.id'], ),
    sa.PrimaryKeyConstraint('story_id', 'rating_type', 'rating')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('story_ratings')
    op.drop_table('story_categories')
    op.drop_table('stories')
    # ### end Alembic commands ###