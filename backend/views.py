from flask import render_template
from backend.models import Cliente

def root():
    return render_template("index.html")
