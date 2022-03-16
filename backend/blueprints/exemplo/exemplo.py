from flask import Blueprint, request, render_template

from backend.ext.database import db
from backend.models import Usuario


bp = Blueprint("exemplo", __name__, url_prefix="/exemplo", template_folder="templates")


@bp.route("/busca/<int:idb>")
def root(idb):
    usuario = Usuario.query.get(idb)
    return f"Usuario: {usuario.nome} <br>Senha: {usuario.senha}"


@bp.route("/salva", methods=["GET", "POST"])
def cadastra():
    if request.method == "POST":
        novo = Usuario()
        novo.nome = request.form["nome"]
        novo.senha = request.form["senha"]

        db.session.add(novo)
        db.session.commit()

        return f"Seu id é: {novo.id}"
    return render_template("exemplo/cadastro.html")


@bp.route("/conversa/<int:idb>/<senha>", methods=["GET", "POST"])
def conversa(idb, senha):
    usuario = Usuario.query.get(idb)

    if usuario and usuario.senha == senha:
        if request.method == "POST":
            pass
        return render_template("exemplo/conversa.html", usu=usuario)

    return "Seu usuário e código de segurança não conferem."


def init_app(app):
    app.register_blueprint(bp)
