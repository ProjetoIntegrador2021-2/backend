from flask import Blueprint


bp = Blueprint('cliente', __name__, url_prefix='/cliente', template_folder='templates')


@bp.route('/')
def root():
    return 'Hello from cliente'


def init_app(app):
    app.register_blueprint(bp)