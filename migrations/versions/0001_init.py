"""Initial migration -- creating tables

Revision ID: 0001_init
Revises: 
Create Date: 2019-03-17 14:24:50.189605

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0001_init'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('artist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=125), nullable=True),
    sa.Column('slug', sa.String(length=150), nullable=True),
    sa.Column('thumbnail', sa.String(length=255), nullable=True),
    sa.Column('hidden', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('slug')
    )
    op.create_table('program',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=60), nullable=False),
    sa.Column('slug', sa.String(length=60), nullable=False),
    sa.Column('href', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('slug')
    )
    op.create_table('episode',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('program_id', sa.Integer(), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['program_id'], ['program.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('song',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=125), nullable=True),
    sa.Column('artist_id', sa.Integer(), nullable=True),
    sa.Column('preview', sa.String(length=255), nullable=True),
    sa.Column('hidden', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('interlude',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('song_id', sa.Integer(), nullable=True),
    sa.Column('order', sa.Integer(), nullable=True),
    sa.Column('episode_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['episode_id'], ['episode.id'], ),
    sa.ForeignKeyConstraint(['song_id'], ['song.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    op.drop_table('interlude')
    op.drop_table('song')
    op.drop_table('episode')
    op.drop_table('program')
    op.drop_table('artist')
    # ### end Alembic commands ###
