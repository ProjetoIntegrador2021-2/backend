from backend.ext.database import db
from backend.ext.auth import login_manager
from flask_login import UserMixin


@login_manager.user_loader
def carregaCliente(id):
    return Cliente.query.get(id)

class Cliente(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(400), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)