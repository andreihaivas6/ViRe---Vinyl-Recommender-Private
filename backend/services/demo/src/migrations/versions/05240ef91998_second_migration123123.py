"""Second migration123123.

Revision ID: 05240ef91998
Revises: 709da38e76ee
Create Date: 2024-01-06 15:31:14.308300

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05240ef91998'
down_revision = '709da38e76ee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('person',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.String(length=32), nullable=True),
    sa.Column('last_name', sa.String(length=32), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('person')
    # ### end Alembic commands ###
