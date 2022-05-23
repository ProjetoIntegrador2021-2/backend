from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from backend.ext.mail import mail
from backend.ext.auth import bcrypt
from backend.models import Cliente, Restaurante, Entregador, Cardapio
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

            return redirect(url_for(''))
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
            return redirect("/cliente/pagina_cliente")
        else:
            return "Senha incorreta"
    else:
        return render_template("cliente/login_cliente.html")


@bp.route("/recuperar_senha", methods=["GET", "POST"])
def recuperar_senha():
    if request.method == "POST":
        email = request.form["email"]

        cliente = Cliente.query.filter_by(email=email).first()

        if not cliente:
            return "Cliente não cadastrado"
        else:
            msg = Message(sender="suporte.flashfood@gmail.com", recipients = [cliente.email])
            msg.html = render_template("cliente/arquivo_email.html", cliente = cliente.id)
            mail.send(msg)
            return redirect("/cliente/recuperar_senha")
    else:
        return render_template("cliente/recuperar_senha.html")

@bp.route("/redefinir_senha/<int:id>", methods=["GET", "POST"])
def redefinir_senha(id):
    recuperacao = Cliente.query.get_or_404(id)
    if request.method == "POST":
        senha_nova = request.form["senha_nova"]
        senha_confirma = request.form["senha_confirma"]

        if senha_nova == senha_confirma:
            senha_criptografada = bcrypt.generate_password_hash(senha_nova)

            recuperacao.senha = senha_criptografada

            db.session.add(recuperacao)
            db.session.commit()

            return redirect("/cliente/login_cliente")
        else:
            return "Erro na redefinição de senha"
    else:
        return render_template("cliente/redefinir_senha.html")


@bp.route("/logout_cliente")
@login_required
def logout_cliente():
    logout_user()
    return "Você saiu da sua conta."


@bp.route("/pagina_cliente")
@login_required
def pagina_cliente():
    cliente=current_user
    restaurante = Restaurante.query.filter_by(cliente_id = cliente.id).first()
    entregador = Entregador.query.filter_by(cliente_id = cliente.id).first()
    cardapio = Cardapio.query.all()

    q = request.args.get("q")
    if q:
        restaurantes = Restaurante.query.filter(Restaurante.nome_restaurante.contains(q))
        cardapios = Cardapio.query.filter(Cardapio.nome_prato.contains(q))
    else:
        restaurantes = Restaurante.query.all()
        cardapios = Cardapio.query.all()

    if restaurante is not None:
        restaurante_verifica = True
    else:
        restaurante_verifica = False

    if entregador is not None:
        entregador_verifica = True
    else:
        entregador_verifica = False

    return render_template("cliente/pagina_cliente.html", restaurante_v=restaurante_verifica, entregador_v=entregador_verifica, restaurante=restaurante, entregador=entregador, restaurantes=restaurantes, cardapios=cardapios, cardapio=cardapio)



@bp.route("/perfil_cliente")
@login_required
def perfil_cliente():
    cliente = current_user
    return render_template("cliente/perfil_cliente.html", cliente=cliente)


@bp.route("/perfil_cliente/editar_perfil/<int:id>", methods = ["GET", "POST"])
@login_required
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

@bp.route('/excluirconta/<int:id>', methods = ["POST"])
@login_required
def excluirconta (id):
    excluir = Cliente.query.get_or_404(id)
    db.session.delete(excluir)
    db.session.commit()

    return 'Você excluiu sua conta, vamos sentir sua falta.'
    #return render_template("cliente/editar_perfil.html", delete=excluir)


def init_app(app):
    app.register_blueprint(bp)