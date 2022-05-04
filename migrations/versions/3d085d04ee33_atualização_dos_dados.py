"""atualização dos dados

Revision ID: 3d085d04ee33
Revises: 0aabb639b657
Create Date: 2022-05-04 00:33:40.789717

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d085d04ee33'
down_revision = '0aabb639b657'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cliente', schema=None) as batch_op:
        batch_op.add_column(sa.Column('CPF', sa.String(length=11), nullable=True))
        batch_op.add_column(sa.Column('Telefone', sa.String(length=11), nullable=True))

    with op.batch_alter_table('entregador', schema=None) as batch_op:
        batch_op.add_column(sa.Column('Contato', sa.String(length=11), nullable=False))
        batch_op.add_column(sa.Column('CPF', sa.String(length=11), nullable=False))
        batch_op.add_column(sa.Column('CNH', sa.String(length=11), nullable=False))
        batch_op.add_column(sa.Column('Telefone', sa.String(length=11), nullable=False))
        batch_op.create_unique_constraint(batch_op.f('uq_entregador_CNH'), ['CNH'])
        batch_op.create_unique_constraint(batch_op.f('uq_entregador_CPF'), ['CPF'])

    with op.batch_alter_table('restaurante', schema=None) as batch_op:
        batch_op.add_column(sa.Column('Categoria', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('CNPJ', sa.String(length=14), nullable=False))
        batch_op.add_column(sa.Column('funcionamento_inicio', sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column('funcionamento_termino', sa.DateTime(), nullable=False))
        batch_op.create_unique_constraint(batch_op.f('uq_restaurante_CNPJ'), ['CNPJ'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('restaurante', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_restaurante_CNPJ'), type_='unique')
        batch_op.drop_column('funcionamento_termino')
        batch_op.drop_column('funcionamento_inicio')
        batch_op.drop_column('CNPJ')
        batch_op.drop_column('Categoria')

    with op.batch_alter_table('entregador', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_entregador_CPF'), type_='unique')
        batch_op.drop_constraint(batch_op.f('uq_entregador_CNH'), type_='unique')
        batch_op.drop_column('Telefone')
        batch_op.drop_column('CNH')
        batch_op.drop_column('CPF')
        batch_op.drop_column('Contato')

    with op.batch_alter_table('cliente', schema=None) as batch_op:
        batch_op.drop_column('Telefone')
        batch_op.drop_column('CPF')

    # ### end Alembic commands ###
