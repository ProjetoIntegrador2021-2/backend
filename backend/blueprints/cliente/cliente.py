from flask import Blueprint, request
from flask_login import login_user
from backend.models import Cliente
from backend.ext.database import db


bp = Blueprint('cliente', __name__, url_prefix="/cliente", template_folder='templates')

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

@bp.route("/login_cliente", methods=["GET", "POST"])
def login_cliente():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        cliente = Cliente.query.filter_by(email=email).first()

        if not cliente:
            return "Cliente não cadastrado",404
        if cliente.senha == senha:
            login_user(cliente)
            return "Deu certo!"

def init_app(app):
    app.register_blueprint(bp)