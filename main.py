from flask import Flask, request, jsonify
from sheets_query import consultar_matricula

app = Flask(__name__)

@app.route("/api/matricula", methods=["POST"])
def api_matricula():
    data = request.get_json()
    identificador = data.get("identificador")
    tipo = data.get("tipo")
    
    if not identificador or not tipo:
        return jsonify({"error": "Faltan parámetros 'identificador' o 'tipo'"}), 400
    
    resultado = consultar_matricula(identificador, tipo)
    return jsonify(resultado)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
