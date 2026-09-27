cat << 'EOF' > main.py
import urllib.request
import json
import datetime
import sqlite3
import threading
import http.server
import socketserver
import time

PORT = 10000
DB_NAME = "rosa_datos.db"
URL_API = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"

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
    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        cursor.execute("SELECT precio FROM historial_eth ORDER BY id DESC LIMIT 5")
        filas = cursor.fetchall()
        conexion.close()
        
        if len(filas) < 2:
            return {"tendencia": "Estable", "variacion": "0.0"}
            
        ultimo = filas[0][0]
        anterior = filas[-1][0]
        diferencia = ((ultimo - anterior) / anterior) * 100
        
        tendencia = "Alcista" if diferencia > 0 else "Bajista" if diferencia < 0 else "Estable"
        return {"tendencia": tendencia, "variacion": f"{diferencia:.2f}%"}
    except Exception:
        return {"tendencia": "N/A", "variacion": "0.0"}

def tarea_segundo_plano():
    inicializar_db()
    while True:
        try:
            req = urllib.request.Request(URL_API, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as respuesta:
                data = json.loads(respuesta.read().decode())
                precio = data["ethereum"]["usd"]
                fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                conexion = sqlite3.connect(DB_NAME)
                cursor = conexion.cursor()
                cursor.execute("INSERT INTO historial_eth (fecha, precio) VALUES (?, ?)", (fecha, precio))
                conexion.commit()
                conexion.close()
                
                analisis = calcular_analisis()
                print(f"[{fecha}] ETH registrado en la nube: ${precio} USD | Tendencia: {analisis.get('tendencia')}")
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
EOF
