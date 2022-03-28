from typing import NoReturn
from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


# Place here the extension's dependencies


# Place here your extension globals
login_manager = LoginManager()
bcrypt = Bcrypt()


def init_app(app: Flask) -> NoReturn:

    """Init your global objects which do need to connect to flask object."""
    login_manager.init_app(app)
    bcrypt.init_app(app)
