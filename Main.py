~/rosa_offline $ nano main.py
~/rosa_offline $ python main.py
Servidor R.O.S.A. activo en el puerto 10000
[2026-09-26 22:44:53] ETH registrado en la nube: $2696.91 USD
^CTraceback (most recent call last):
  File "/data/data/com.termux/files/home/rosa_offline/main.py", line 74, in <module>
    run()
    ~~~^^
  File "/data/data/com.termux/files/home/rosa_offline/main.py", line 71, in run
    servidor.serve_forever()
    ~~~~~~~~~~~~~~~~~~~~~~^^
  File "/data/data/com.termux/files/usr/lib/python3.14/socketserver.py", line 235, in serve_forever
    ready = selector.select(poll_interval)
  File "/data/data/com.termux/files/usr/lib/python3.14/selectors.py", line 398, in select
    fd_event_list = self._selector.poll(timeout)
KeyboardInterrupt

~/rosa_offline $ nano main.py
~/rosa_offline $ python main.py
Traceback (most recent call last):
  File "/data/data/com.termux/files/home/rosa_offline/main.py", line 1, in <module>
    http.server
    ^^^^
NameError: name 'http' is not defined. Did you forget to import 'http'?
~/rosa_offline $ nano main.py
~/rosa_offline $ python main.py
Servidor y Analizador R.O.S.A. activos en el puerto 10000
[2026-09-26 22:48:37] ETH: $2696.38 USD | Tendencia: BAJISTA 📉
[2026-09-26 22:53:37] ETH: $2695.73 USD | Tendencia: BAJISTA 📉
[2026-09-26 22:58:39] ETH: $2696.3 USD | Tendencia: BAJISTA 📉
[2026-09-26 23:03:39] ETH: $2695.81 USD | Tendencia: BAJISTA 📉
^CTraceback (most recent call last):
  File "/data/data/com.termux/files/home/rosa_offline/main.py", line 106, in <module>
    run()
    ~~~^^
  File "/data/data/com.termux/files/home/rosa_offline/main.py", line 103, in run
    servidor.serve_forever()
    ~~~~~~~~~~~~~~~~~~~~~~^^
  File "/data/data/com.termux/files/usr/lib/python3.14/socketserver.py", line 235, in serve_forever                                                                                 ready = selector.select(poll_interval)                                                File "/data/data/com.termux/files/usr/lib/python3.14/selectors.py", line 398, in select
    fd_event_list = self._selector.poll(timeout)
KeyboardInterrupt                                                                       
~/rosa_offline $ touch requirements.txt
~/rosa_offline $ git init
git add main.py requirements.txt
git commit -m "Servidor Rosa v1"
hint: Using 'master' as the name for the initial branch. This default branch name
hint: will change to "main" in Git 3.0. To configure the initial branch name
hint: to use in all of your new repositories, which will suppress this warning,
hint: call:
hint:
hint:   git config --global init.defaultBranch <name>                                   hint:
hint: Names commonly chosen instead of 'master' are 'main', 'trunk' and
hint: 'development'. The just-created branch can be renamed via this command:           hint:
hint:   git branch -m <name>
hint:
hint: Disable this message with "git config set advice.defaultBranchName false"
Initialized empty Git repository in /data/data/com.termux/files/home/rosa_offline/.git/
Author identity unknown

*** Please tell me who you are.

Run

  git config --global user.email "you@example.com"
  git config --global user.name "Your Name"

to set your account's default identity.
Omit --global to set the identity only in this repository.

fatal: unable to auto-detect email address (got 'u0_a335@localhost.(none)')
~/rosa_offline $ git config --global user.email "rosa@server.com"                       git config --global user.name "Rosa Server"
~/rosa_offline $ git commit -m "Servidor Rosa v1"
[master (root-commit) 504bfaa] Servidor Rosa v1
 2 files changed, 106 insertions(+)
 create mode 100644 main.py
 create mode 100644 requirements.txt
~/rosa_offline $ git remote add origin https://github.com/armanbotello4-create/rosa-server.git
 git branch -M main
git push -u origin main
Username for 'https://github.com': armanbotello4-create
Password for 'https://armanbotello4-create@github.com':
~/rosa_offline $ main.py
main.py: command not found
~/rosa_offline $ cat main.py
import http.server
import socketserver
import urllib.request
import json
import sqlite3
import threading
import time
import os
from datetime import datetime

PORT = int(os.environ.get("PORT", 10000))
URL_API = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
DB_NAME = "rosa_datos.db"

def inicializar_db():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historial_eth (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            precio REAL
        )
    """)
    conexion.commit()
    conexion.close()

def calcular_analisis():
    """Calcula tendencia rápida y niveles estimados de TP / SL basados en los últimos registros"""
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("SELECT precio FROM historial_eth ORDER BY id DESC LIMIT 5")
    filas = cursor.fetchall()
    conexion.close()

    if not filas or len(filas) < 2:
        return {"estado": "Acumulando datos...", "tendencia": "NEUTRAL"}

    precios = [f[0] for f in filas]
    precio_actual = precios[0]
    sma = sum(precios) / len(precios)

    tendencia = "ALCISTA 📈" if precio_actual >= sma else "BAJISTA 📉"

    if "ALCISTA" in tendencia:
        tp = precio_actual * 1.015
        sl = precio_actual * 0.992
    else:
        tp = precio_actual * 0.985
        sl = precio_actual * 1.008

    return {
        "precio_actual": precio_actual,
        "media_movil_5": round(sma, 2),
        "tendencia": tendencia,
        "Take_Profit_TP": round(tp, 2),
        "Stop_Loss_SL": round(sl, 2)
    }

def tarea_segundo_plano():
    inicializar_db()
    while True:
        try:
            req = urllib.request.Request(URL_API, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as respuesta:
                data = json.loads(respuesta.read().decode())
                precio = data["ethereum"]["usd"]
                fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                conexion = sqlite3.connect(DB_NAME)
                cursor = conexion.cursor()
                cursor.execute("INSERT INTO historial_eth (fecha, precio) VALUES (?, ?)", (fecha, precio))
                conexion.commit()
                conexion.close()

                analisis = calcular_analisis()
                print(f"[{fecha}] ETH: ${precio} USD | Tendencia: {analisis.get('tendencia', 'N/A')}")
        except Exception as e:
            print(f"Error en consulta: {e}")

        time.sleep(300)

hilo = threading.Thread(target=tarea_segundo_plano, daemon=True)
hilo.start()

class Manejador(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        resultado_analisis = calcular_analisis()
        respuesta = {
            "robot": "R.O.S.A. Core",
            "activo": "Ethereum (ETH)",
            "analisis_mercado": resultado_analisis
        }
        self.wfile.write(json.dumps(respuesta, indent=4).encode("utf-8"))

def run():
    servidor = socketserver.TCPServer(("", PORT), Manejador)
    print(f"Servidor y Analizador R.O.S.A. activos en el puerto {PORT}")
    servidor.serve_forever()

if __name__ == "__main__":
    run()
~/rosa_offline $
