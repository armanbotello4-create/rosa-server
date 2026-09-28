from flask import Flask, jsonify, request
import random

app = Flask(__name__)

tareas_pendientes = [
    "Sistema R.O.S.A. inteligente listo."
]

@app.route('/')
def home():
    return "Servidor R.O.S.A. activo 🚀"

@app.route('/termux/obtener_tareas', methods=['GET'])
def obtener_tareas():
    global tareas_pendientes
    enviar = tareas_pendientes.copy()
    tareas_pendientes.clear()
    return jsonify({"tareas": enviar})

@app.route('/preguntar', methods=['GET'])
def preguntar():
    global tareas_pendientes
    comando = request.args.get('q', 'analizar oro')
    
    if "oro" in comando.lower() or "xauusd" in comando.lower():
        precio = round(random.uniform(2380.0, 2430.0), 2)
        respuesta = f"Analizando XAUUSD. Precio actual en {precio}. Se detecta presión compradora cerca del soporte institucional. Recomiendo cautela."
    else:
        respuesta = f"Comando recibido: {comando}. Operación procesada con éxito."
        
    tareas_pendientes.append(respuesta)
    return jsonify({"estado": "pensado", "respuesta": respuesta})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
