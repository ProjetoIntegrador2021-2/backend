from typing import NoReturn
from flask import Flask
from flask_mail import Mail

# Place here the extension's dependencies

mail = Mail()

# Place here your extension globals


def init_app(app : Flask) -> NoReturn:
    '''Init your global objects which do need to connect to flask object.'''
    mail.init_app(app)