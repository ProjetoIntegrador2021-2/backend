from flask import render_template
from backend.models import Cliente
from backend.models import Entregador

def root():
    return render_template("index.html")
