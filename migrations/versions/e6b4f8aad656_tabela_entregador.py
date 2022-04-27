"""Tabela Entregador

Revision ID: e6b4f8aad656
Revises: 5d978d234b7d
Create Date: 2022-04-26 00:14:26.172120

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6b4f8aad656'
down_revision = '5d978d234b7d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('entregador',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Veiculo', sa.Boolean(), nullable=True),
    sa.Column('Regiao', sa.Boolean(), nullable=True),
    sa.Column('cliente_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cliente_id'], ['cliente.id'], name=op.f('fk_entregador_cliente_id_cliente')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_entregador'))
    )
    with op.batch_alter_table('cliente', schema=None) as batch_op:
        batch_op.add_column(sa.Column('Nome', sa.String(length=400), nullable=False))
        batch_op.add_column(sa.Column('Email', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('Senha', sa.String(length=100), nullable=False))
        batch_op.drop_constraint('uq_cliente_email', type_='unique')
        batch_op.create_unique_constraint(batch_op.f('uq_cliente_Email'), ['Email'])
        batch_op.drop_column('nome')
        batch_op.drop_column('senha')
        batch_op.drop_column('email')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cliente', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.VARCHAR(length=100), nullable=False))
        batch_op.add_column(sa.Column('senha', sa.VARCHAR(length=100), nullable=False))
        batch_op.add_column(sa.Column('nome', sa.VARCHAR(length=400), nullable=False))
        batch_op.drop_constraint(batch_op.f('uq_cliente_Email'), type_='unique')
        batch_op.create_unique_constraint('uq_cliente_email', ['email'])
        batch_op.drop_column('Senha')
        batch_op.drop_column('Email')
        batch_op.drop_column('Nome')

    op.drop_table('entregador')
    # ### end Alembic commands ###