from flask import render_template
from backend.models import Cliente
from backend.models import Entregador
from backend.models import Restaurante
from backend.models import Cardapio

def root():
    return render_template("index.html")

