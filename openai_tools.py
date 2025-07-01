# openai_tools.py

import requests

def buscar_estudiante(identificador, tipo):
    url = "https://project-sheets.onrender.com/api/matricula"
    payload = {
        "identificador": identificador,
        "tipo": tipo
    }
    response = requests.post(url, json=payload)
    return response.json()
