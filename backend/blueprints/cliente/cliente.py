from flask import Blueprint, request
from backend.models import Cliente
from backend.ext.database import db


bp = Blueprint('cliente', __name__, url_prefix='/cliente', template_folder='templates')


@bp.route("/cadastro_cliente", methods=["GET", "POST"])
def cadastro_cliente():
    if request.method == "POST":
        novo = Cliente()
        novo.nome = request.form["nome"]
        novo.email = request.form["email"]
        novo.senha = request.form["senha"]

        db.session.add(novo)
        db.session.commit()

        return "Bem-vindo ao FoodFlash"
    else:
        return "Não deu certo"


def init_app(app):
    app.register_blueprint(bp)