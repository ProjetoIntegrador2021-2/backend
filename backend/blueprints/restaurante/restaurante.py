from flask import Blueprint, request, redirect, render_template
from backend.models import Restaurante, Cliente
from backend.ext.auth import bcrypt
from flask_login import login_user
from backend.ext.database import db


bp = Blueprint('restaurante', __name__, url_prefix='/restaurante', template_folder='templates')


@bp.route("login_restaurante/cadastro_restaurante", methods=["GET", "POST"])
def cadastro_restaurante():
    cidades = {
        "-------": "--------",
        "Aracati": "ARACATI",
        "Fortim": "FORTIM",
        "Icapuí": "ICAPUÍ",
        }

    categorias = {
        "-------":"-------",
        "pizza": "PIZZA",
        "doces":"DOCES",
        "hamburguer":"HAMBURGUER",
        }
    if request.method == "POST":
        email= request.form["email"]
        senha= request.form["senha"]

        cliente= Cliente.query.filter_by(email=email).first()

        if not cliente:
            return "Você não é cadastrado como cliente"
        else:
            novo = Restaurante()
            novo.nome_restaurante = request.form["nome_restaurante"]
            novo.endereco = request.form["endereco"]
            novo.cidade = request.form.get("cidade")
            novo.categoria = request.form.get("categoria")
            novo.cnpj = request.form["cnpj"]
            novo.funcionamento_inicio = request.form["funcionamento_inicio"]
            novo.funcionamento_termino = request.form["funcionamento_termino"]
            novo.cliente_id = cliente.id

            db.session.add(novo)
            db.session.commit()

        return redirect("/restaurante/pagina_restaurante")
    else:
        return render_template("restaurante/cadastro_restaurante.html", cidades=cidades, categorias=categorias)

@bp.route("/login_restaurante", methods=["GET", "POST"])
def login_restaurante():
    if request.method == "POST":
        email=request.method["email"]
        senha=request.method["senha"]

        restaurante = Restaurante.query.filter_by(cliente_id = email).first()

        if not restaurante:
            return "Restaurante não cadastrado", 404

        if bcrypt.check_password_hash(restaurante.senha, senha):
            login_user(restaurante)
            return redirect("/restaurante/pagina_restaurante")
    else:
        return render_template("restaurante/login_restaurante.html")

@bp.route("/pagina_restaurante")
def pagina_restaurante():
    return render_template("restaurante/pagina_restaurante.html")


def init_app(app):
    app.register_blueprint(bp)