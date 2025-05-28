import tkinter as tk
from tkinter import messagebox
import json
import requests
from utils import get_ip_address
import subprocess

# Carregar dados do config.json
with open('config.json', 'r') as f:
    config = json.load(f)

# URL do servidor Flask
SERVIDOR_URL = 'http://127.0.0.1:5000/agente/'  # Troque pelo IP real do servidor ADM se necessário


def enviar_requisicao():
    dados = {
        "ip_serv": config["ip_serv"],
        "marca_comp": config["marca_comp"],
        "so_comp": config["so_comp"],
        "cor_comp": config["cor_comp"]
    }

    try:
        resposta = requests.post(SERVIDOR_URL, json=dados)

        if resposta.status_code == 200:
            messagebox.showinfo("Conectado", "Requisição enviada ao servidor com sucesso!")

            # Iniciar monitoramento após aceitação
            subprocess.Popen(["python", "monitoramento.py"])

        else:
            messagebox.showerror("Erro", f"Falha ao enviar requisição: {resposta.status_code}\n{resposta.text}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro de conexão: {str(e)}")


# Interface Tkinter
janela = tk.Tk()
janela.title("Agente TeleGuard")
janela.geometry("300x200")

label = tk.Label(janela, text="Agente do Telecentro", font=("Arial", 14))
label.pack(pady=20)

btn = tk.Button(janela, text="Requisição ao Servidor", command=enviar_requisicao, bg="blue", fg="white", padx=10,
                pady=5)
btn.pack()

janela.mainloop()