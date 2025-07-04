"""Add content field to Task

Revision ID: e72bed7466c1
Revises: 0ac403055144
Create Date: 2025-04-17 15:05:43.941737

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e72bed7466c1'
down_revision = '0ac403055144'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('content', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('theme_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['theme_id'], ['themes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('tasks')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tasks',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(length=200), autoincrement=False, nullable=False),
    sa.Column('type', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('theme_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['theme_id'], ['themes.id'], name='tasks_theme_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='tasks_pkey')
    )
    op.drop_table('task')
    # ### end Alembic commands ###
