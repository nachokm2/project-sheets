import gspread
from oauth2client.service_account import ServiceAccountCredentials

def consultar_matricula(identificador, tipo):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", scope)
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
