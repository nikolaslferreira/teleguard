from .auth import auth_bp
from .agente import agente_bp
from flask import Blueprint

def init_routes(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(agente_bp, url_prefix='/agente')
