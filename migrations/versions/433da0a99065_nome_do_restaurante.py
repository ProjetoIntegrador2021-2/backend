"""nome do restaurante

Revision ID: 433da0a99065
Revises: 71c7aef9b005
Create Date: 2022-05-08 21:47:58.860094

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '433da0a99065'
down_revision = '71c7aef9b005'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('restaurante', schema=None) as batch_op:
        batch_op.add_column(sa.Column('Nome do restaurante', sa.String(length=400), nullable=False))
        batch_op.drop_column('Nome')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('restaurante', schema=None) as batch_op:
        batch_op.add_column(sa.Column('Nome', sa.VARCHAR(length=400), nullable=False))
        batch_op.drop_column('Nome do restaurante')

    # ### end Alembic commands ###
