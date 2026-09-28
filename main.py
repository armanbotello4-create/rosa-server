from flask import Flask, jsonify, request
import random

app = Flask(__name__)

# Cola de tareas pendientes para que Termux las lea y hable
tareas_pendientes = [
    "Núcleo R.O.S.A. inicializado correctamente."
]

@app.route('/')
def home():
    return "Servidor R.O.S.A. API Activo 🚀"

@app.route('/termux/obtener_tareas', methods=['GET'])
def obtener_tareas():
    global tareas_pendientes
    enviar = tareas_pendientes.copy()
    tareas_pendientes.clear()
    return jsonify({"tareas": enviar})

@app.route('/preguntar', methods=['GET'])
def preguntar():
    global tareas_pendientes
    # Recibe la consulta que le mandes desde Termux
    comando = request.args.get('q', 'analizar oro')
    
    # Lógica de análisis simulada (puedes conectarla a una API de trading más adelante)
    if "oro" in comando.lower() or "xauusd" in comando.lower():
        precio = round(random.uniform(2380.0, 2430.0), 2)
        respuesta = f"Análisis de XAUUSD. Cotizando en {precio}. Tendencia con soporte firme. Operación viable."
    else:
        respuesta = f"Comando procesado con éxito: {comando}."
        
    # Agrega la respuesta a la cola para que el celular la hable
    tareas_pendientes.append(respuesta)
    return jsonify({"estado": "ok", "respuesta": respuesta})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
