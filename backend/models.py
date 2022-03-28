from backend.ext.database import db
from backend.ext.auth import login_manager
from flask_login import UserMixin


@login_manager.user_loader
def carregaUsuario(id):
    return Usuario.query.get(id)


class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    nome_completo = db.Column(db.String(400))

    mensagens = db.relationship("Mensagem", backref="usuario", lazy=True)


class Mensagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(144), nullable=False)

    remetente = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    conversa_id = db.Column(db.Integer, db.ForeignKey("conversa.id"))


class Conversa(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    part_a_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    part_b_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

    mensagens = db.relationship("Mensagem", backref="conversa", lazy=True)
