"""mudança

Revision ID: 0aabb639b657
Revises: dbc464232a60
Create Date: 2022-04-28 22:41:13.142507

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0aabb639b657'
down_revision = 'dbc464232a60'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('restaurante', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cliente_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('uq_restaurante_Email', type_='unique')
        batch_op.create_foreign_key(batch_op.f('fk_restaurante_cliente_id_cliente'), 'cliente', ['cliente_id'], ['id'])
        batch_op.drop_column('Email')
        batch_op.drop_column('Senha')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('restaurante', schema=None) as batch_op:
        batch_op.add_column(sa.Column('Senha', sa.VARCHAR(length=100), nullable=False))
        batch_op.add_column(sa.Column('Email', sa.VARCHAR(length=100), nullable=False))
        batch_op.drop_constraint(batch_op.f('fk_restaurante_cliente_id_cliente'), type_='foreignkey')
        batch_op.create_unique_constraint('uq_restaurante_Email', ['Email'])
        batch_op.drop_column('cliente_id')

    # ### end Alembic commands ###
