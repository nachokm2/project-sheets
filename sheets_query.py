import os
import json
import gspread
from google.oauth2.service_account import Credentials

def consultar_matricula(identificador, tipo):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # Leer el JSON desde variable de entorno
    raw_creds = os.getenv("GOOGLE_CREDS_JSON")
    if not raw_creds:
        return {"error": "No se encontraron credenciales en la variable de entorno."}
    
    creds_dict = json.loads(raw_creds)
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    
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
