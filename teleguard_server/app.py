from flask import Flask
from flask_cors import CORS
from routes.computers import computers_bp
from teleguard_server.routes.auth import auth_bp
from routes.agente import agente_bp
import subprocess
import time
import os

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_teleguard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'chave_super_secreta'

app.register_blueprint(computers_bp, url_prefix="/api/computers")
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(agente_bp, url_prefix="/agente")

@app.route('/')
def home():
    return 'Servidor Teleguard está ativo!'

if __name__ == '__main__':
    app.run(debug=True)
