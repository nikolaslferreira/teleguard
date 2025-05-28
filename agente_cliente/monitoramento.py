import webbrowser
import time
import mitmproxy
from mitmproxy import http, ctx, addons
from mitmproxy.tools.main import mitmdump
import threading

# Lista de sites proibidos
SITES_PROIBIDOS = [
    "xvideos.com",
    "pornhub.com",
    "redtube.com",
    "onlyfans.com",
    "xhamster.com"
]

# Abrir navegador Chrome (modo normal)
def abrir_chrome():
    webbrowser.open("http://www.google.com")

# Addon do mitmproxy
class Bloqueador:
    def request(self, flow: http.HTTPFlow) -> None:
        host = flow.request.pretty_host
        for site in SITES_PROIBIDOS:
            if site in host:
                ctx.log.info(f"Bloqueado: {host}")
                flow.response = http.Response.make(
                    403,
                    "<h1>ACESSO BLOQUEADO</h1><p>Este site está proibido neste telecentro.</p>".encode('utf-8'),
                    {"Content-Type": "text/html; charset=utf-8"}
                )

def iniciar_mitmproxy():
    addons = [Bloqueador()]

if __name__ == "__main__":
    abrir_chrome()
    time.sleep(10000)
    print("[INFO] Iniciando bloqueio de sites proibidos...")
    threading.Thread(target=iniciar_mitmproxy).start()

