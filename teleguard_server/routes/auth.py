from flask import Blueprint, request, jsonify
from teleguard_server.db import get_connection
from datetime import datetime
import socket

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    rg = data.get('RG_FUNC')
    senha = data.get('SENHA')

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT ID_FUNC, NOME_FUNC FROM FUNCIONARIO WHERE RG_FUNC = ? AND SENHA = ?", (rg, senha))
        result = cursor.fetchone()

        if result:
            id_func, nome_func = result

            agora = datetime.now()
            data_atual = agora.strftime('%Y-%m-%d')
            hora_atual = agora.strftime('%H:%M:%S')

            ip_serv = socket.gethostbyname(socket.gethostname())

            cursor.execute("SELECT * FROM SERVIDOR WHERE IP_SERV = ?", (ip_serv,))
            servidor_existente = cursor.fetchone()

            if not servidor_existente:
                cursor.execute(
                    """INSERT INTO SERVIDOR 
                       (IP_SERV, DATA_INIC, HORA_INIC, DATA_TERM, HORA_TERM, ID_FUNC) 
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (ip_serv, data_atual, hora_atual, '0000-00-00', '--:--:--', id_func)
                )
                print(f"Novo servidor registrado com IP: {ip_serv}")

            cursor.execute(
                """INSERT INTO LOGIN (ID_FUNC, IP_SERV, DATA_LOGIN, HORA_LOGIN)
                   VALUES (?, ?, ?, ?)""",
                (id_func, ip_serv, data_atual, hora_atual)
            )

            conn.commit()

            return jsonify({
                "mensagem": "Login realizado com sucesso!",
                "NOME_FUNC": nome_func
            }), 200
        else:
            return jsonify({"mensagem": "RG ou senha inválidos."}), 401

    except Exception as e:
        return jsonify({"mensagem": f"Erro no servidor: {str(e)}"}), 500

    finally:
        conn.close()
