"""empty message

Revision ID: bc551d51f28c
Revises: 458fd35d4fd1
Create Date: 2017-08-22 23:46:46.624787

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc551d51f28c'
down_revision = '458fd35d4fd1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('episodes', sa.Column('seasonId', sa.Integer(), nullable=True))
    op.alter_column('episodes', 'title',
               existing_type=sa.VARCHAR(length=180),
               nullable=False)
    op.drop_constraint('episodes_season_id_fkey', 'episodes', type_='foreignkey')
    op.create_foreign_key(None, 'episodes', 'seasons', ['seasonId'], ['id'])
    op.drop_column('episodes', 'season_id')
    op.alter_column('seasons', 'title',
               existing_type=sa.VARCHAR(length=200),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('seasons', 'title',
               existing_type=sa.VARCHAR(length=200),
               nullable=True)
    op.add_column('episodes', sa.Column('season_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'episodes', type_='foreignkey')
    op.create_foreign_key('episodes_season_id_fkey', 'episodes', 'seasons', ['season_id'], ['id'])
    op.alter_column('episodes', 'title',
               existing_type=sa.VARCHAR(length=180),
               nullable=True)
    op.drop_column('episodes', 'seasonId')
    # ### end Alembic commands ###
