from flask import Blueprint


bp = Blueprint('entregador', __name__, url_prefix='/entregador', template_folder='templates')


@bp.route('/')
def root():
    return 'Hello from entregador'


def init_app(app):
    app.register_blueprint(bp)