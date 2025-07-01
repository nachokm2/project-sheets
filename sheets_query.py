import os
import json
import gspread
from google.oauth2.service_account import Credentials

def consultar_matricula(identificador, tipo):
    raw_creds = os.environ["GOOGLE_CREDS"]
    # Importante: si tu variable tiene "\\n", reemplázalos por "\n"
    raw_creds = raw_creds.replace("\\n", "\n")

    creds_dict = json.loads(raw_creds)
    creds = Credentials.from_service_account_info(creds_dict, scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ])

    client = gspread.authorize(creds)
    sheet = client.open("Copia de 2025 CONSOLIDADO MATRÍCULAS POSTGRADOS CHILE").worksheet("MATRÍCULAS CHILE")
    data = sheet.get_all_records()

    for fila in data:
        if tipo == "correo" and fila["CORREO"].strip().lower() == identificador.strip().lower():
            return fila
        elif tipo == "rut" and str(fila["RUT"]).strip() == str(identificador).strip():
            return fila
        elif tipo == "nombre" and identificador.lower() in (fila["NOMBRES"] + " " + fila["APELLIDOS"]).lower():
            return fila

    return {"error": "No se encontró información con ese identificador."}
