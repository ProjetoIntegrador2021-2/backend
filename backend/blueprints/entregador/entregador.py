from flask import Blueprint, request
from backend.models import Entregador
from backend.ext.database import db


bp = Blueprint(
    "entregador",
    __name__,
    url_prefix="/entregador",
    template_folder="templates",
)


@bp.route("/cadastro_entregador", methods=["GET", "POST"])
def cadastro_entregador():
    if request.method == "POST":
        novo = Entregador()
        novo.veiculo = request.form["veiculo"]
        novo.regiao = request.form["regiao"]

        db.session.add(novo)
        db.session.commit()

        return "Bem-vindo ao Flash Food, entregador! Venha gastar sua gasolina com a gente!"
    else:
        return "Dança da motinha"


def init_app(app):
    app.register_blueprint(bp)
