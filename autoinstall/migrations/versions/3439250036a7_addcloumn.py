"""addcloumn

Revision ID: 3439250036a7
Revises: 84f21fd30b8
Create Date: 2017-06-12 05:38:49.320264

"""

# revision identifiers, used by Alembic.
revision = '3439250036a7'
down_revision = '84f21fd30b8'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hosts', sa.Column('general_user', sa.String(length=32), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('hosts', 'general_user')
    ### end Alembic commands ###
