import os
import json
import gspread
from google.oauth2.service_account import Credentials

def consultar_matricula(identificador, tipo):
    # Validar tipo de búsqueda
    tipos_validos = {"correo", "rut", "nombre"}
    if tipo not in tipos_validos:
        return {"error": f"Tipo de búsqueda '{tipo}' no válido. Debe ser uno de {tipos_validos}"}

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    try:
        # Leer credenciales desde variable de entorno
        raw_creds = os.getenv("GOOGLE_CREDS_JSON")
        if not raw_creds:
            return {"error": "No se encontraron credenciales en la variable de entorno."}

        creds_dict = json.loads(raw_creds)
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        client = gspread.authorize(creds)

        # Abrir hoja de cálculo y worksheet
        sheet = client.open("Copia de 2025 CONSOLIDADO MATRÍCULAS POSTGRADOS CHILE").worksheet("MATRÍCULAS CHILE")
        data = sheet.get_all_records()

        # Buscar registro según tipo
        for fila in data:
            if tipo == "correo" and fila.get("CORREO", "").strip().lower() == identificador.strip().lower():
                return fila
            elif tipo == "rut" and str(fila.get("RUT", "")).strip() == str(identificador).strip():
                return fila
            elif tipo == "nombre" and identificador.lower() in (fila.get("NOMBRES", "") + " " + fila.get("APELLIDOS", "")).lower():
                return fila

        return {"error": "No se encontró información con ese identificador."}

    except Exception as e:
        return {"error": f"Error al consultar la hoja: {str(e)}"}
