from flask import Blueprint, request, render_template

from backend.ext.database import db
from backend.models import Usuario, Mensagem, Conversa


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
        conversas = Conversa.query.filter_by(part_a_id=idb).all()
        if request.method == "POST":
            pass
        return render_template("exemplo/conversa.html", usu=usuario, conv=conversas)

    return "Seu usuário e código de segurança não conferem."


@bp.route("/mensagem/<int:idu>/<texto>")
def mensagem(idu, texto):
    remetente = Usuario.query.get(idu)

    nova = Mensagem()
    nova.remetente = remetente.id
    nova.texto = texto

    db.session.add(nova)
    db.session.commit()

    return "mensagem enviada"


@bp.route("/minhasmensagens/<int:idu>")
def minhas(idu):
    usuario = Usuario.query.get(idu)

    resposta = ""
    for mensagem in usuario.mensagens:
        resposta += f"{mensagem.texto}<br>"
    return resposta


@bp.route("/criaconversa/<int:ida>/<int:idb>")
def criaconversa(ida, idb):
    um = Usuario.query.get(ida)
    dois = Usuario.query.get(idb)

    nova = Conversa()
    nova.part_a_id = um.id
    nova.part_b_id = dois.id

    db.session.add(nova)
    db.session.commit()

    return "Conversa criada."


def init_app(app):
    app.register_blueprint(bp)
