from backend.ext.database import db


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    nome_completo = db.Column(db.String(400))
