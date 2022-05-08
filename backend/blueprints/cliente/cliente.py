from flask import Blueprint, request, render_template, redirect
from flask_login import login_user, logout_user
from backend.ext.auth import bcrypt
from backend.models import Cliente
from backend.ext.database import db


bp = Blueprint('cliente', __name__, url_prefix="/cliente", template_folder='templates')

@bp.route("/")
def home():
    return render_template("cliente/home.html")

@bp.route("login_cliente/cadastro_cliente", methods=["GET", "POST"])
def cadastro_cliente():
    if request.method == "POST":
        novo = Cliente()
        novo.nome = request.form["nome"]
        novo.email = request.form["email"]
        senha_adicionada = request.form["senha"]
        senha_confirma = request.form["senha_confirma"]

        if senha_adicionada == senha_confirma:

            senha_criptografada = bcrypt.generate_password_hash(senha_adicionada)

            novo.senha = senha_criptografada

            db.session.add(novo)
            db.session.commit()

            return redirect("/cliente/pagina_cliente")
        else:
            return "Erro na confirmação de senha"
    else:
        return render_template("cliente/cadastro_cliente.html")

@bp.route("/login_cliente", methods=["GET", "POST"])
def login_cliente():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        cliente = Cliente.query.filter_by(email=email).first()

        if not cliente:
            return "Cliente não cadastrado",404

        if bcrypt.check_password_hash(cliente.senha, senha):
            login_user(cliente)
            return redirect ("/cliente/pagina_cliente")
    else:
        return render_template("cliente/login_cliente.html")
@bp.route("/logout_cliente")
def logout_cliente():
    logout_user()
    return "Você saiu da sua conta."

@bp.route("/pagina_cliente")
def pagina_cliente():
    return render_template("cliente/pagina_cliente.html")

@bp.route("/perfil_cliente")
def perfil_cliente():
    cliente = Cliente()
    return render_template("cliente/perfil_cliente.html", cliente=cliente)

@bp.route("/perfil_cliente/editar_perfil/<int:id>", methods = ["GET", "POST"])
def editar_perfil(id):
    edit = Cliente.query.get_or_404(id)
    if request.method == "POST":
        edit.nome = request.form["nome"]
        edit.endereco = request.form["endereco"]
        edit.cpf = request.form["cpf"]
        edit.telefone = request.form["telefone"]
        try:
            db.session.add(edit)
            db.session.commit()
            return redirect("/cliente/perfil_cliente")
        except:
            return "Não deu certo o update"
    else:
        return render_template("cliente/editar_perfil.html", cliente=edit)

def init_app(app):
    app.register_blueprint(bp)