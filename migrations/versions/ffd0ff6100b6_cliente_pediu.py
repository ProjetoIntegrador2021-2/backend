"""cliente pediu

Revision ID: ffd0ff6100b6
Revises: d31510fa0db3
Create Date: 2022-06-20 13:16:42.639694

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ffd0ff6100b6'
down_revision = 'd31510fa0db3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pedidofeito', schema=None) as batch_op:
        batch_op.add_column(sa.Column('Cliente', sa.String(length=400), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pedidofeito', schema=None) as batch_op:
        batch_op.drop_column('Cliente')

    # ### end Alembic commands ###
