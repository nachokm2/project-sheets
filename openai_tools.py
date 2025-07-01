import requests

def buscar_estudiante(identificador, tipo):
    url = "https://project-sheets.onrender.com/api/matricula"
    payload = {
        "identificador": identificador,
        "tipo": tipo
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()  # Lanza error si status != 200
        return response.json()
    except requests.exceptions.Timeout:
        return {"error": "La solicitud a la API tardó demasiado y fue cancelada."}
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"Error HTTP al consultar la API: {http_err}"}
    except Exception as e:
        return {"error": f"Error inesperado al consultar la API: {str(e)}"}
