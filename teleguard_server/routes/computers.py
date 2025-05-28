from flask import Blueprint, jsonify

computers_bp = Blueprint('computers', __name__)

@computers_bp.route('/')
def list_computers():
    return jsonify({"message": "Lista de computadores"})
