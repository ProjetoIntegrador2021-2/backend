from flask import Blueprint, request, redirect, render_template
from backend.models import Restaurante, Cliente, Cardapio
from flask_login import current_user
from backend.ext.database import db


bp = Blueprint('restaurante', __name__, url_prefix='/restaurante', template_folder='templates')


@bp.route("/cadastro_restaurante", methods=["GET", "POST"])
def cadastro_restaurante():
    cidades = {
        "-------": "--------",
        "Aracati": "Aracati",
        "Fortim": "Fortim",
        "Icapuí": "Icapuí",
        }
    categorias = {
        "-------": "--------",
        "Japonesa": "Japonesa",
        "Bebidas": "Bebidas",
        "Lanches": "Lanches",
        "Carnes": "Carnes",
        "Doces": "Doces",
        "Pizzas": "Pizzas",
        }
    if request.method == "POST":
        email= request.form["email"]

        cliente= Cliente.query.filter_by(email=email).first()

        if not cliente:
           return redirect("/cliente/login_cliente/cadastro_cliente")
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

        return redirect("/cliente/pagina_cliente")
    else:
        return render_template("restaurante/cadastro_restaurante.html", cidades=cidades, categorias=categorias)


@bp.route("/pagina_restaurante/<int:id>")
def pagina_restaurante(id):
    restaurante = Restaurante.query.get_or_404(id)
    #restaurantes = Restaurante.query.filter_by(cliente_id = current_user.id).first()
    cardapio=Cardapio.query.all()
    cardapios = Cardapio.query.filter_by(restaurante_id = restaurante.id).all()
    return render_template("restaurante/pagina_restaurante.html", restaurante=restaurante, cardapio=cardapio, cardapios=cardapios)

@bp.route("/perfil_restaurante/")
def perfil_restaurante():
    cliente = current_user
    restaurante = Restaurante.query.filter_by(cliente_id = cliente.id).first()
    return render_template("restaurante/perfil_restaurante.html", restaurante=restaurante)

@bp.route("/perfil_restaurante/editar_perfil/<int:id>", methods=["GET", "POST"])
def editar_perfil(id):
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
    edit = Restaurante.query.get_or_404(id)
    if request.method == "POST":
        edit.nome_restaurante = request.form["nome_restaurante"]
        edit.endereco = request.form["endereco"]
        edit.cidade = request.form.get("cidade")
        edit.categoria = request.form.get("categoria")
        edit.funcionamento_inicio = request.form["funcionamento_inicio"]
        edit.funcionamento_termino = request.form["funcionamento_termino"]
        try:
            db.session.add(edit)
            db.session.commit()
            return redirect ("/restaurante/perfil_restaurante")
        except:
            return "Não deu certo o update"
    else:
        return render_template("restaurante/editar_perfil.html", restaurante=edit, cidades=cidades, categorias=categorias)

@bp.route("/pagina_restaurante/adicionar_cardapio", methods=["GET","POST"])
def adicionar_cardapio():
    cliente = current_user
    restaurante = Restaurante.query.filter_by(cliente_id = cliente.id).first()
    if request.method == "POST":
        novo=Cardapio()
        novo.nome_prato = request.form["nome_prato"]
        novo.valor = request.form["valor"]
        novo.ingredientes = request.form["ingredientes"]
        novo.tempo_preparo = request.form["tempo_preparo"]
        novo.restaurante_id = restaurante.id

        db.session.add(novo)
        db.session.commit()
        return redirect("/restaurante/pagina_restaurante/adicionar_cardapio")
    else:
        return render_template("restaurante/adicionar_cardapio.html")

def init_app(app):
    app.register_blueprint(bp)