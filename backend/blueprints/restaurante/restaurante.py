from flask import Blueprint, request
from backend.models import Restaurante
from backend.ext.database import db


bp = Blueprint(
    "restaurante",
    __name__,
    url_prefix="/restaurante",
    template_folder="templates",
)


@bp.route("/cadastro_restaurante", methods=["GET", "POST"])
def cadastro_restaurante():
    if request.method == "POST":
        novo = Restaurante()
        novo.nome = request.form["nome"]
        novo.endereco = request.form["endereco"]
        novo.cidade = request.form["cidade"]

        db.session.add(novo)
        db.session.commit()

        return "Boas vendas!"
    else:
        return "Não tenham boas vendas"


def init_app(app):
    app.register_blueprint(bp)
