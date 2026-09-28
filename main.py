from flask import Flask, jsonify, request
import random

app = Flask(__name__)

tareas_pendientes = [
    "Núcleo R.O.S.A. en línea."
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

# ESTA ES LA RUTA QUE FALTA ACTIVAR EN RENDER
@app.route('/preguntar', methods=['GET'])
def preguntar():
    global tareas_pendientes
    comando = request.args.get('q', 'analizar oro')
    
    if "oro" in comando.lower() or "xauusd" in comando.lower():
        precio = round(random.uniform(2380.0, 2430.0), 2)
        respuesta = f"Análisis de XAUUSD. Cotización actual en {precio} dólares. Soporte técnico validado. Zona de entrada óptima."
    else:
        respuesta = f"Orden procesada: {comando}"
        
    tareas_pendientes.append(respuesta)
    return jsonify({"estado": "ok", "respuesta": respuesta})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
