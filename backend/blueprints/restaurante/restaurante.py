from flask import Blueprint


bp = Blueprint('restaurante', __name__, url_prefix='/restaurante', template_folder='templates')


@bp.route('/')
def root():
    return 'Hello from restaurante'


def init_app(app):
    app.register_blueprint(bp)