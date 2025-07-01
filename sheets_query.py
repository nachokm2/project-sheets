import os
import json
import gspread
from google.oauth2.service_account import Credentials

def consultar_matricula(identificador, tipo):
    # Cargar las credenciales desde la variable de entorno (Render)
    creds_dict = json.loads(os.environ["GOOGLE_CREDS"])

    # Autenticación moderna
    creds = Credentials.from_service_account_info(creds_dict)
    client = gspread.authorize(creds)

    # Acceder a la hoja
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
