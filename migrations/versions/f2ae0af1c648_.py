"""empty message

Revision ID: f2ae0af1c648
Revises: 
Create Date: 2024-03-01 07:41:29.351316

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2ae0af1c648'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stores',
    sa.Column('store_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('store_id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('items',
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('price', sa.Float(precision=2), nullable=False),
    sa.Column('store_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['store_id'], ['stores.store_id'], ),
    sa.PrimaryKeyConstraint('item_id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('tags',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('store_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['store_id'], ['stores.store_id'], ),
    sa.PrimaryKeyConstraint('tag_id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('item_tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=True),
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['items.item_id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.tag_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('item_tags')
    op.drop_table('tags')
    op.drop_table('items')
    op.drop_table('users')
    op.drop_table('stores')
    # ### end Alembic commands ###
