"""Initial migration.

Revision ID: 079df2912c1f
Revises: e25c18df002c
Create Date: 2024-02-02 15:41:53.648514

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '079df2912c1f'
down_revision = 'e25c18df002c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('playlists', schema=None) as batch_op:
        batch_op.drop_column('timestamp')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('playlists', schema=None) as batch_op:
        batch_op.add_column(sa.Column('timestamp', sa.DATETIME(), nullable=True))

    # ### end Alembic commands ###
