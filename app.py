from flask import Flask, request, jsonify
from sheets_query import consultar_matricula  # Asegúrate de tener esta función bien definida

app = Flask(__name__)

@app.route("/api/matricula", methods=["POST"])
def api_matricula():
    data = request.get_json()
    identificador = data.get("identificador")
    tipo = data.get("tipo")  # debe ser "correo", "rut" o "nombre"

    if not identificador or not tipo:
        return jsonify({"error": "Faltan parámetros 'identificador' o 'tipo'"}), 400

    resultado = consultar_matricula(identificador, tipo)
    return jsonify(resultado)

if __name__ == "__main__":
    from os import getenv
    port = int(getenv("PORT", 5000))  # Puerto asignado por Render, 5000 por defecto si no existe
    app.run(host="0.0.0.0", port=port)
