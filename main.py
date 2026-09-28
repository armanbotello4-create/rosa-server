from flask import Flask, jsonify
import random

app = Flask(__name__)

# Cola de tareas pendientes para Termux
tareas_pendientes = [
    "Módulo de trading de R.O.S.A. sincronizado en la nube."
]

@app.route('/')
def home():
    return "Servidor R.O.S.A. de Trading activo 📈"

@app.route('/termux/obtener_tareas', methods=['GET'])
def obtener_tareas():
    global tareas_pendientes
    enviar = tareas_pendientes.copy()
    tareas_pendientes.clear()
    return jsonify({"tareas": enviar})

@app.route('/enviar_orden/<mensaje>', methods=['GET'])
def enviar_orden(mensaje):
    tareas_pendientes.append(mensaje)
    return jsonify({"estado": "enviado", "orden": mensaje})

# NUEVA RUTA: Analiza el oro (XAUUSD) desde la nube y crea la orden de voz automáticamente
@app.route('/analizar_oro', methods=['GET'])
def analizar_oro():
    global tareas_pendientes
    
    # Aquí puedes conectar luego una API real de precios (como MetaTrader o Alpha Vantage)
    # Por ahora, simularemos un análisis técnico inteligente basado en acción de precio:
    precio_actual = round(random.uniform(2350.0, 2450.0), 2)
    tendencias = ["alcista con rebote en soporte clave", "en rango de consolidación esperando ruptura", "bajista testeando zona de alta liquidez"]
    tendencia_elegida = random.choice(tendencias)
    
    reporte = f"Atención. Análisis de oro XAUUSD. Precio actual aproximado en {precio_actual}. El mercado se encuentra {tendencia_elegida}. Monitorear niveles de entrada."
    
    # Inyecta el reporte automáticamente a la cola para que Termux hable
    tareas_pendientes.append(reporte)
    
    return jsonify({
        "estado": "analizado", 
        "precio": precio_actual, 
        "reporte": reporte
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
