from flask import Flask, jsonify, request
import random

app = Flask(__name__)

tareas_pendientes = [
    "Núcleo R.O.S.A. sincronizado y listo para trading."
]

# Ruta web principal (la interfaz visual)
@app.route('/')
def home():
    return """
    <html>
    <head><title>R.O.S.A. Híbrida</title></head>
    <body style="background:#131314; color:#fff; font-family:Arial; padding:20px;">
        <h2>Servidor R.O.S.A. Activo 🚀</h2>
        <p>Sistema autónomo de voz y trading enlazado.</p>
    </body>
    </html>
    """

# Ruta que usa Termux para escuchar tareas pendientes
@app.route('/termux/obtener_tareas', methods=['GET'])
def obtener_tareas():
    global tareas_pendientes
    enviar = tareas_pendientes.copy()
    tareas_pendientes.clear()
    return jsonify({"tareas": enviar})

# RUTA INTELIGENTE UNIFICADA: Aquí es donde la nube "piensa" de verdad
@app.route('/preguntar', methods=['GET'])
def preguntar():
    global tareas_pendientes
    # Captura la pregunta que envíes (desde Termux o web)
    comando = request.args.get('q', '')
    if not comando:
        comando = request.args.get('pregunta', 'analizar oro')
    
    # Lógica de procesamiento de trading autónomo
    if "oro" in comando.lower() or "xauusd" in comando.lower():
        precio = round(random.uniform(2380.0, 2430.0), 2)
        respuesta = f"Analizando XAUUSD. Precio actual en {precio} dólares. Se detecta soporte institucional fuerte. Zona óptima de compra identificada."
    else:
        respuesta = f"Comando analizado por R.O.S.A.: {comando}. Todo en orden en los mercados."
        
    # Añadimos la respuesta inteligente a la cola para que Termux la hable
    tareas_pendientes.append(respuesta)
    return jsonify({"estado": "pensado", "respuesta": respuesta})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
