from flask import Blueprint

from backend.ext.database import db
from backend.models import Usuario


bp = Blueprint("exemplo", __name__, url_prefix="/exemplo", template_folder="templates")


@bp.route("/busca/<int:id>")
def root(id):
    usuario = Usuario.query.get(id)
    return f"Usuario: {usuario.nome} <br>Senha: {usuario.senha}"


@bp.route("/salva/<nome>/<senha>")
def cadastra(nome, senha):
    novo = Usuario()
    novo.nome = nome
    novo.senha = senha

    db.session.add(novo)
    db.session.commit()

    return "deu certo"


def init_app(app):
    app.register_blueprint(bp)
