from flask import Blueprint, request, render_template, redirect
from flask_login import login_user
from backend.models import Entregador, Cliente
from backend.ext.auth import bcrypt
from backend.ext.database import db



bp = Blueprint('entregador', __name__, url_prefix='/entregador', template_folder='templates')

@bp.route('/parceria')
def parceria():
    return render_template('entregador/parceria.html')

@bp.route('/login_entregador/cadastro_entregador', methods=["GET", "POST"])
def cadastro_entregador():
    regioes = {
    '--------': '--------',
    'Aracati':'ARACATI',
    'Fortim':'FORTIM',
    'Icapuí': 'ICAPUÍ',
    }
    if request.method == "POST":
        email=request.form["email"]
        senha=request.form["senha"]

        cliente= Cliente.query.filter_by(email=email).first()
        if not cliente:
            return "Você não é cadastrado como cliente"
        else:
            novo = Entregador()
            novo.regiao = request.form.get('regiao')
            novo.contato = request.form["contato"]
            novo.cpf = request.form["cpf"]
            novo.cnh = request.form["cnh"]
            novo.veiculo = request.form["veiculo"]
            novo.cliente_id = cliente.id

            db.session.add(novo)
            db.session.commit()

            return redirect("/entregador/pagina_entregador")
    else:
        return render_template("entregador/cadastro_entregador.html", regioes=regioes)

@bp.route('/login_entregador', methods=["GET", "POST"])
def login_entregador():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        entregador = Entregador.query.filter_by(cliente_id=email).first()

        if not entregador:
            return "Entregador não cadastrado", 404

        if bcrypt.check_password_hash(entregador.senha, senha):
            login_user(entregador)
            return redirect ("/entregador/pagina_entregador")
    else:
        return render_template("entregador/login_entregador.html")

@bp.route("/pagina_entregador")
def pagina_entregador():
    return render_template("entregador/pagina_entregador.html")

def init_app(app):
    app.register_blueprint(bp)