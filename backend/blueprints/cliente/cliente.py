import os
from backend.app import create_app
from flask import Blueprint, request, render_template, redirect, url_for, flash, send_from_directory, session
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from backend.ext.mail import mail
from backend.ext.auth import bcrypt
from backend.models import Cliente, Restaurante, Entregador, Cardapio, Pedidofeito
from backend.ext.database import db
import mercadopago
from werkzeug.utils import secure_filename

bp = Blueprint('cliente', __name__, url_prefix="/cliente", template_folder='templates')

ALLOWED_EXTENSIONS = {'png', 'jpeg', 'jpg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route("/")
def home():
    return render_template("cliente/home-page.html")


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

            return redirect("/cliente/login_cliente")
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
            return redirect(url_for('cliente.pagina_cliente', id=cliente.id))
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
            return redirect("/cliente/email_sucesso")
    else:
        return render_template("cliente/recuperar_senha.html")

@bp.route("/email_sucesso")
def email_sucesso():
    return render_template("cliente/email_enviado.html")


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


@bp.route("/logout_cliente", methods=["GET","POST"])
@login_required
def logout_cliente():
    if request.method == "POST":
        logout_user()

        return redirect("/cliente")


@bp.route("/pagina_cliente/<int:id>")
@login_required
def pagina_cliente(id):
    cliente=Cliente.query.get_or_404(id)
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

    return render_template("cliente/cliente-page.html", q=q,  restaurante_v=restaurante_verifica, entregador_v=entregador_verifica, restaurante=restaurante, entregador=entregador, restaurantes=restaurantes, cardapios=cardapios, cardapio=cardapio)

@bp.route("/pega_nome/<int:id>")
def pega_nome(id):
    pega_id = Cardapio.query.get_or_404(id)
    restaurante = Restaurante.query.filter_by(id=pega_id.restaurante_id).first()
    return send_from_directory(restaurante=restaurante)


@bp.route("/upload/<int:id>/<path:filename>")
@login_required
def upload(id,filename):
    app = create_app()
    return send_from_directory(app.config['UPLOAD_FOLDER'], id, filename)


@bp.route("/salvar_pedido/<int:id>", methods=["GET", "POST"])
@login_required
def salvar_pedido(id):
    cardapio = Cardapio.query.get_or_404(id)
    session['pedido'] = float(cardapio.valor.replace(",", ".")) * int(request.form["quantidade"]) + 2
    session['description'] = f'{cardapio.nome_prato} x {request.form["quantidade"]}'
    if request.method == "POST":
        novo = Pedidofeito()
        novo.nome_pedido = cardapio.nome_prato
        novo.valor_pedido = cardapio.valor
        novo.restaurante_id = cardapio.restaurante_id
        novo.cliente_id = current_user.id

        db.session.add(novo)
        db.session.commit()
        return redirect(url_for('cliente.cadastro_endereco', id=novo.id))
    else:
        return "NÃO DEU CERTO"
        '''
        session['nome_prato'] = cardapio.nome_prato
        session['valor'] = cardapio.valor
        session['cliente_id'] = current_user.id
        session['restaurante_id'] = cardapio.restaurante_id
        '''


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
        if 'imagem_perfil' not in request.files:
            flash('No file part')
            return redirect(request.url)
        imagem_perfil = request.files["imagem_perfil"]
        edit.nome = request.form["nome"]
        edit.endereco = request.form["endereco"]
        edit.cpf = request.form["cpf"]
        edit.telefone = request.form["telefone"]
        try:

            if imagem_perfil.filename == '':
                flash('No selected file')
                return redirect(request.url)

            if imagem_perfil and allowed_file(imagem_perfil.filename):
                filename = secure_filename(imagem_perfil.filename)
                app = create_app()
                imagem_perfil.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                edit.imagem_perfil = filename

                db.session.add(edit)
                db.session.commit()

                return redirect("/cliente/perfil_cliente")
        except:
            return "Não deu certo o update"
    else:
        return render_template("cliente/editar_perfil.html", cliente=edit)

@bp.route("/detalhe_cardapio/<int:id>", methods=["GET", "POST"])
@login_required
def detalhe_cardapio(id):
    pega_id = Cardapio.query.get_or_404(id)
    session['pedido'] = pega_id
    restaurante = Restaurante.query.filter_by(id=pega_id.restaurante_id).first()
    if request.method == "POST":
        novo = Pedidofeito()
        novo.nome_pedido = pega_id.nome_prato
        novo.valor_pedido = pega_id.valor
        novo.restaurante_id = pega_id.restaurante_id
        novo.cliente_id = current_user.id

        db.session.add(novo)
        db.session.commit()
        return redirect(url_for('cliente.cadastro_endereco', id=novo.id))
    else:
        return render_template("cliente/pagina_cliente.html", pega_id=pega_id, restaurante=restaurante)


@bp.route('/excluirconta/<int:id>', methods = ["POST"])
@login_required
def excluirconta(id):
    excluir = Cliente.query.get_or_404(id)
    db.session.delete(excluir)
    db.session.commit()

    return 'Você excluiu sua conta, vamos sentir sua falta.'
    #return render_template("cliente/editar_perfil.html", delete=excluir)

@bp.route("/pagina_restaurante/<int:id>")
def pagina_restaurante(id):
    restaurante = Restaurante.query.get_or_404(id)
    cardapio=Cardapio.query.all()
    cardapios = Cardapio.query.filter_by(restaurante_id = restaurante.id).all()

    q = request.args.get("q")

    if q:
        cardapios_get = Cardapio.query.filter_by(restaurante_id=restaurante.id).filter(Cardapio.nome_prato.contains(q))
    else:
        cardapios_get = cardapios

    return render_template("cliente/pagina-restaurante.html", restaurante=restaurante, cardapio=cardapio, cardapios=cardapios_get)


@bp.route("/cadastre_endereco/<int:id>", methods=["GET", "POST"])
@login_required
def cadastro_endereco(id):
    adicionar = Pedidofeito.query.get_or_404(id)
    if request.method == "POST":
        adicionar.endereco = request.form["endereco"]
        adicionar.cliente_pediu = current_user.nome
        try:
            db.session.add(adicionar)
            db.session.commit()
            return redirect(url_for('cliente.pagina_pagamento', id=current_user.id))
        except:
            return "Não deu certo confirmar endereço"
    else:
        return render_template("cliente/cadastro_endereco.html")

@bp.route("/pagina_pagamento/<int:id>", methods=["GET", "POST"])
@login_required
def pagina_pagamento(id):
    cliente_pagar = Cliente.query.get_or_404(id)

    banco_emissor = [
        "Mastercard", "Visa", "American Express",
        ]

    documento = [
        "CPF", "RG",
        ]

    parcela = [
        "1x", "2x",
        ]
    if request.method == "POST":
        sdk = mercadopago.SDK("TEST-2722201582418152-061511-781d1859bffe7a2bcd68fd6765a420ca-1142330935")

        payment_data = {
            "transaction_amount":float(request.get_json()["transaction_amount"]),
            "token": request.get_json()["token"],
            "description": request.get_json()["description"],
            "installments": int(request.get_json()["installments"]),
            "payment_method_id": request.get_json()["payment_method_id"],
            "payer": {
                "email": request.get_json()["payer"]["email"],
                "identification": {
                    "type": request.get_json()["payer"]["identification"]["type"],
                    "number": request.get_json()["payer"]["identification"]["number"]
                }
            }
        }

        payment_response = sdk.payment().create(payment_data)
        payment = payment_response["response"]
        print(payment)

        return payment
        #return redirect(url_for('cliente.pagina_cliente', id=cliente_pagar.id))
    else:
        return render_template("cliente/pagina_pagamento.html", cliente_pagar=cliente_pagar, banco_emissores=banco_emissor, documentos=documento, parcelas=parcela)

@bp.route("/categoria")
@login_required
def categoria():
    restaurante = Restaurante.query.all()
    restaurantes = Restaurante.query.filter(Restaurante.categoria.contains("Lanches"))
    return render_template("cliente/categorias.html", restaurante=restaurante, restaurantes=restaurantes)

def init_app(app):
    app.register_blueprint(bp)