import http.server
import socketserver
import urllib.request
import json
import datetime
import sqlite3
import threading
import time
from urllib.parse import urlparse, parse_qs

PORT = 10000
DB_NAME = "rosa_datos.db"
URL_API = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"

# Memoria temporal en la nube para tareas pendientes hacia Termux
tareas_pendientes = []
resultados_termux = []

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
        except Exception as e:
            print(f"Error en segundo plano: {e}")
        time.sleep(300)

hilo = threading.Thread(target=tarea_segundo_plano, daemon=True)
hilo.start()

HTML_CHAT = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>R.O.S.A. Híbrida - Cloud & Mobile</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #131314; color: #e3e3e3; margin: 0; padding: 0; display: flex; flex-direction: column; height: 100vh; }
        header { background-color: #1e1f20; padding: 15px; text-align: center; font-size: 1.2rem; font-weight: bold; border-bottom: 1px solid #333; color: #a8c7fa; }
        #chat-container { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 15px; max-width: 800px; width: 100%; margin: 0 auto; box-sizing: border-box; }
        .message { padding: 12px 18px; border-radius: 15px; max-width: 75%; line-height: 1.5; word-wrap: break-word; }
        .user { background-color: #004a77; color: #fff; align-self: flex-end; border-bottom-right-radius: 2px; }
        .rosa { background-color: #1e1f20; color: #e3e3e3; align-self: flex-start; border-bottom-left-radius: 2px; border: 1px solid #333; }
        #input-container { background-color: #1e1f20; padding: 15px; display: flex; justify-content: center; border-top: 1px solid #333; }
        #input-box { width: 100%; max-width: 750px; display: flex; background: #2b2c2f; border-radius: 25px; padding: 5px 15px; border: 1px solid #444; }
        input[type="text"] { flex: 1; background: transparent; border: none; color: #fff; padding: 10px; font-size: 1rem; outline: none; }
        button { background-color: #a8c7fa; color: #131314; border: none; padding: 10px 20px; border-radius: 20px; font-weight: bold; cursor: pointer; transition: 0.2s; }
        button:hover { background-color: #8ab4f8; }
    </style>
</head>
<body>
    <header>R.O.S.A. Núcleo Híbrido (Cloud + Termux)</header>
    <div id="chat-container">
        <div class="message rosa">¡Hola! Soy R.O.S.A. Conectada a la nube y lista para enviar órdenes a tu celular vía Termux.</div>
    </div>
    <div id="input-container">
        <div id="input-box">
            <input type="text" id="user-input" placeholder="Escribe una orden para tu celular o pregunta..." onkeydown="if(event.key === 'Enter') enviarMensaje()">
            <button onclick="enviarMensaje()">Enviar</button>
        </div>
    </div>
    <script>
        async function enviarMensaje() {
            const input = document.getElementById('user-input');
            const container = document.getElementById('chat-container');
            const texto = input.value.trim();
            if(!texto) return;

            container.innerHTML += `<div class="message user">${texto}</div>`;
            input.value = '';
            container.scrollTop = container.scrollHeight;

            try {
                const res = await fetch(`/api?pregunta=${encodeURIComponent(texto)}`);
                const data = await res.json();
                
                let respuestaTexto = data.mensaje || "Orden procesada.";
                container.innerHTML += `<div class="message rosa">${respuestaTexto}</div>`;
            } catch (err) {
                container.innerHTML += `<div class="message rosa">Error de comunicación con el servidor.</div>`;
            }
            container.scrollTop = container.scrollHeight;
        }
    </script>
</body>
</html>
"""

class Manejador(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        url_path = urlparse(self.path)
        parametros = parse_qs(url_path.query)
        
        # 1. API para el Chat Web
        if url_path.path == "/api":
            pregunta = parametros.get("pregunta", [""])[0].lower()
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            
            respuesta = {}
            if "clima" in pregunta:
                respuesta = {"mensaje": "El clima en la nube está despejado y listo."}
            elif "ethereum" in pregunta:
                an = calcular_analisis()
                respuesta = {"mensaje": f"Ethereum - Tendencia: {an['tendencia']}, Variación: {an['variacion']}"}
            else:
                # Mandar la orden a la cola para que Termux la recoja
                tareas_pendientes.append(pregunta)
                respuesta = {"mensaje": f"Orden '{pregunta}' registrada en la nube. Esperando que Termux la ejecute en tu celular..."}
                
            self.wfile.write(json.dumps(respuesta).encode("utf-8"))

        # 2. Endpoints para que Termux se comunique con la Nube
        elif url_path.path == "/termux/obtener_tareas":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            # Enviar tareas pendientes y vaciar la lista
            pendientes = list(tareas_pendientes)
            tareas_pendientes.clear()
            self.wfile.write(json.dumps({"tareas": pendientes}).encode("utf-8"))

        elif url_path.path == "/termux/enviar_resultado":
            res_texto = parametros.get("resultado", [""])[0]
            resultados_termux.append(res_texto)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"estado": "recibido"}).encode("utf-8"))

        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_CHAT.encode("utf-8"))

def run():
    servidor = socketserver.TCPServer(("", PORT), Manejador)
    print(f"R.O.S.A. Híbrida activa en el puerto {PORT}")
    servidor.serve_forever()

if __name__ == "__main__":
    run()
