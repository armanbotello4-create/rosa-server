from flask import Flask, jsonify

app = Flask(__name__)

# Lista donde se acumularán las órdenes para tu celular
tareas_pendientes = [
    "Sistema R.O.S.A. en línea y conectado con éxito."
]

@app.route('/')
def home():
    return "Servidor R.O.S.A. activo 🚀"

@app.route('/termux/obtener_tareas', methods=['GET'])
def obtener_tareas():
    global tareas_pendientes
    enviar = tareas_pendientes.copy()
    tareas_pendientes.clear()  # Limpia la lista para que no se repitan
    return jsonify({"tareas": enviar})

@app.route('/enviar_orden/<mensaje>', methods=['GET'])
def enviar_orden(mensaje):
    tareas_pendientes.append(mensaje)
    return jsonify({"estado": "enviado", "orden": mensaje})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
