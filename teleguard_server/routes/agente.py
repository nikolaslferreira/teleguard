from flask import Blueprint, jsonify, request
import sqlite3

agente_bp = Blueprint('agente', __name__)

DB_PATH = 'db_teleguard.db'

@agente_bp.route('/requests', methods=['GET'])
def listar_requisicoes():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT ID_COMP, MARCA_COMP, SO_COMP, COR_COMP FROM COMPUTADOR WHERE STATUS_CONEXAO = 'pendente'")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([{
        "id_comp": row[0],
        "marca": row[1],
        "so": row[2],
        "cor": row[3]
    } for row in rows]), 200

@agente_bp.route('/accept/<int:id_comp>', methods=['POST'])
def aceitar(id_comp):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE COMPUTADOR SET STATUS_CONEXAO = 'aceito' WHERE ID_COMP = ?", (id_comp,))
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Computador aceito"}), 200

@agente_bp.route('/computers', methods=['GET'])
def listar_conectados():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT ID_COMP, MARCA_COMP, SO_COMP, COR_COMP, IP_SERV FROM COMPUTADOR WHERE STATUS_CONEXAO = 'aceito'")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([{
        "id_comp": row[0],
        "marca": row[1],
        "so": row[2],
        "cor": row[3],
        "ip": row[4]
    } for row in rows]), 200

@agente_bp.route('/disconnect/<int:id_comp>', methods=['POST'])
def desconectar(id_comp):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE COMPUTADOR SET STATUS_CONEXAO = 'desconectado' WHERE ID_COMP = ?", (id_comp,))
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Desconectado com sucesso"}), 200

@agente_bp.route('/', methods=['POST'])
def receber_requisicao():
    dados = request.get_json()

    ip_serv = dados.get("ip_serv")
    marca = dados.get("marca_comp")
    so = dados.get("so_comp")
    cor = dados.get("cor_comp")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Inserir ou atualizar a máquina como pendente
    cursor.execute("""
        INSERT INTO COMPUTADOR (IP_SERV, MARCA_COMP, SO_COMP, COR_COMP, STATUS_CONEXAO)
        VALUES (?, ?, ?, ?, 'pendente')
    """, (ip_serv, marca, so, cor))

    conn.commit()
    conn.close()

    print(f"Nova requisição recebida: {ip_serv}")
    return jsonify({"mensagem": "Requisição recebida com sucesso!"}), 200

@agente_bp.route('/', methods=['POST'])
def registrar_computador():
    dados = request.get_json()
    ip = request.remote_addr
    marca = dados.get('marca')
    cor = dados.get('cor')
    so = dados.get('so')

    conn = sqlite3.connect('db_teleguard.db')
    cursor = conn.cursor()

    cursor.execute("INSERT OR IGNORE INTO COMPUTADOR (IP, MARCA, COR, SO, STATUS) VALUES (?, ?, ?, ?, ?)",
                   (ip, marca, cor, so, 'pendente'))

    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Requisição de conexão registrada"}), 200

@agente_bp.route('/status/<ip>', methods=['GET'])
def verificar_status(ip):
    conn = sqlite3.connect('db_teleguard.db')
    cursor = conn.cursor()

    cursor.execute("SELECT STATUS FROM COMPUTADOR WHERE IP = ?", (ip,))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        return jsonify({"status": resultado[0]})
    else:
        return jsonify({"erro": "Computador não encontrado"}), 404
