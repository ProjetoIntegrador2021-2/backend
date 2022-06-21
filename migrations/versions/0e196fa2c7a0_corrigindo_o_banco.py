"""Corrigindo o banco

Revision ID: 0e196fa2c7a0
Revises: 
Create Date: 2022-06-21 22:37:03.216914

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e196fa2c7a0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cliente',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Nome', sa.String(length=400), nullable=False),
    sa.Column('Email', sa.String(length=100), nullable=False),
    sa.Column('imagem_perfil', sa.String(length=100), nullable=True),
    sa.Column('Senha', sa.String(length=100), nullable=False),
    sa.Column('CPF', sa.String(length=11), nullable=True),
    sa.Column('Telefone', sa.String(length=11), nullable=True),
    sa.Column('Endereço', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_cliente')),
    sa.UniqueConstraint('Email', name=op.f('uq_cliente_Email'))
    )
    op.create_table('entregador',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Veículo', sa.String(length=100), nullable=True),
    sa.Column('Região', sa.String(length=100), nullable=True),
    sa.Column('Contato', sa.String(length=11), nullable=False),
    sa.Column('CPF', sa.String(length=11), nullable=False),
    sa.Column('CNH', sa.String(length=11), nullable=False),
    sa.Column('cliente_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cliente_id'], ['cliente.id'], name=op.f('fk_entregador_cliente_id_cliente')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_entregador')),
    sa.UniqueConstraint('CNH', name=op.f('uq_entregador_CNH')),
    sa.UniqueConstraint('CPF', name=op.f('uq_entregador_CPF'))
    )
    op.create_table('restaurante',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Nome do restaurante', sa.String(length=400), nullable=False),
    sa.Column('Endereço', sa.String(length=200), nullable=False),
    sa.Column('Cidade ', sa.String(length=100), nullable=True),
    sa.Column('Categorias', sa.String(length=100), nullable=True),
    sa.Column('imagem_perfil', sa.String(length=100), nullable=True),
    sa.Column('CNPJ', sa.String(length=14), nullable=False),
    sa.Column('Abre:', sa.String(length=6), nullable=False),
    sa.Column('Fecha:', sa.String(length=6), nullable=False),
    sa.Column('cliente_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cliente_id'], ['cliente.id'], name=op.f('fk_restaurante_cliente_id_cliente')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_restaurante')),
    sa.UniqueConstraint('CNPJ', name=op.f('uq_restaurante_CNPJ'))
    )
    op.create_table('cardapio',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Nome do prato', sa.String(length=400), nullable=False),
    sa.Column('Valor do prato', sa.String(length=10), nullable=False),
    sa.Column('imagem_prato', sa.String(length=100), nullable=True),
    sa.Column('Ingredientes', sa.String(length=500), nullable=False),
    sa.Column('Tempo de preparo', sa.String(length=6), nullable=False),
    sa.Column('Restaurante_adicionou', sa.String(length=400), nullable=True),
    sa.Column('Categorias', sa.String(length=100), nullable=True),
    sa.Column('restaurante_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['restaurante_id'], ['restaurante.id'], name=op.f('fk_cardapio_restaurante_id_restaurante')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_cardapio'))
    )
    op.create_table('pedidofeito',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Nome do pedido', sa.String(length=400), nullable=False),
    sa.Column('Valor do pedido', sa.String(length=10), nullable=False),
    sa.Column('Endereço', sa.String(length=200), nullable=True),
    sa.Column('Nome do cliente', sa.String(length=400), nullable=True),
    sa.Column('restaurante_id', sa.Integer(), nullable=True),
    sa.Column('cliente_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cliente_id'], ['cliente.id'], name=op.f('fk_pedidofeito_cliente_id_cliente')),
    sa.ForeignKeyConstraint(['restaurante_id'], ['restaurante.id'], name=op.f('fk_pedidofeito_restaurante_id_restaurante')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_pedidofeito'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pedidofeito')
    op.drop_table('cardapio')
    op.drop_table('restaurante')
    op.drop_table('entregador')
    op.drop_table('cliente')
    # ### end Alembic commands ###