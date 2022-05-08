from backend.ext.database import db
from backend.ext.auth import login_manager
from flask_login import UserMixin


@login_manager.user_loader

def carregaCliente(id):
    return Cliente.query.get(id)

def carregaEntregador(id):
    return Entregador.query.get(id)

def carregaRestaurante(id):
    return Restaurante.query.get(id)


class Cliente(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column("Nome", db.String(400), nullable=False)
    email = db.Column("Email", db.String(100), unique=True, nullable=False)
    senha = db.Column("Senha", db.String(100), nullable=False)
    cpf = db.Column("CPF", db.String(11))
    telefone = db.Column("Telefone", db.String(11))
    endereco = db.Column("Endereço", db.String(200))

class Entregador(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    veiculo = db.Column("Veiculo", db.Boolean, default=False)
    regiao = db.Column("Regiao", db.Boolean, default=False)
    contato = db.Column("Contato", db.String(11), nullable=False)
    cpf = db.Column("CPF", db.String(11), nullable = False, unique = True)
    cnh = db.Column("CNH", db.String(11), unique = True, nullable = False)

    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"))

class Restaurante(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome_restaurante = db.Column('Nome do restaurante', db.String(400), nullable=False)
    endereco = db.Column('Endereço', db.String(200), nullable=False)
    cidade = db.Column('Cidade', db.Boolean, default=False)
    categoria = db.Column('Categoria', db.Boolean, default = False)
    cnpj = db.Column('CNPJ', db.String(14), unique = True, nullable=False)
    funcionamento_inicio = db.Column(db.DateTime, nullable=False)
    funcionamento_termino = db.Column(db.DateTime, nullable=False)

    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"))

