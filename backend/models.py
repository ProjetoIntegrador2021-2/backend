from backend.ext.database import db
from backend.ext.auth import login_manager
from flask_login import UserMixin


@login_manager.user_loader

def carregaCliente(id):
    return Cliente.query.get(id)

class Cliente(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column("Nome", db.String(400), nullable=False)
    email = db.Column("Email", db.String(100), unique=True, nullable=False)
    imagem_perfil = db.Column(db.String(100), nullable=True)
    senha = db.Column("Senha", db.String(100), nullable=False)
    cpf = db.Column("CPF", db.String(11))
    telefone = db.Column("Telefone", db.String(11))
    endereco = db.Column("Endereço", db.String(200))

    restaurante = db.relationship("Restaurante", backref="cliente", lazy=True)
    entregador = db.relationship("Entregador", backref="cliente", lazy=True)

class Entregador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    veiculo = db.Column("Veículo", db.String(100))
    regiao = db.Column("Região", db.String(100))
    contato = db.Column("Contato", db.String(11), nullable=False)
    cpf = db.Column("CPF", db.String(11), nullable = False, unique = True)
    cnh = db.Column("CNH", db.String(11), unique = True, nullable = False)

    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"))

class Restaurante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_restaurante = db.Column('Nome do restaurante', db.String(400), nullable=False)
    endereco = db.Column('Endereço', db.String(200), nullable=False)
    cidade = db.Column('Cidade ', db.String(100))
    categoria = db.Column('Categorias', db.String(100))
    imagem_perfil = db.Column(db.String(100), nullable=True)
    cnpj = db.Column('CNPJ', db.String(14), unique = True, nullable=False)
    funcionamento_inicio = db.Column('Abre:', db.String(6), nullable=False)
    funcionamento_termino = db.Column('Fecha:', db.String(6), nullable=False)

    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"))

    cardapios = db.relationship("Cardapio", backref="restaurante", lazy=True)

class Cardapio(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    nome_prato=db.Column("Nome do prato",db.String(400), nullable=False)
    valor=db.Column("Valor do prato", db.String(10), nullable=False)
    imagem_prato = db.Column(db.String(100), nullable=True)
    ingredientes = db.Column("Ingredientes", db.String(500), nullable=False)
    tempo_preparo = db.Column("Tempo de preparo", db.String(6), nullable=False)
    restaurante_adicionou = db.Column("Restaurante_adicionou", db.String(400), nullable=True)
    restaurante_categoria = db.Column('Categorias', db.String(100), nullable=True)

    restaurante_id = db.Column(db.Integer, db.ForeignKey("restaurante.id"))

class Pedidofeito(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    nome_pedido=db.Column("Nome do pedido",db.String(400), nullable=False)
    valor_pedido=db.Column("Valor do pedido", db.String(10), nullable=False)
    endereco=db.Column("Endereço", db.String(200), nullable=True)
    cliente_pediu = db.Column("Nome do cliente", db.String(400), nullable=True)

    restaurante_id = db.Column(db.Integer, db.ForeignKey("restaurante.id"))
    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"))
