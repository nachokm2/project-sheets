import os
import json
import gspread
from google.oauth2.service_account import Credentials

def consultar_matricula(identificador, tipo):
    tipos_validos = {"correo", "rut", "nombre"}
    if tipo not in tipos_validos:
        return {"error": f"Tipo de búsqueda '{tipo}' no válido. Debe ser uno de {tipos_validos}"}

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    try:
        raw_creds = os.getenv("GOOGLE_CREDS_JSON")
        if not raw_creds:
            return {"error": "No se encontraron credenciales en la variable de entorno."}

        creds_dict = json.loads(raw_creds)
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        client = gspread.authorize(creds)

        sheet = client.open("Copia de 2025 CONSOLIDADO MATRÍCULAS POSTGRADOS CHILE").worksheet("MATRÍCULAS CHILE")
        data = sheet.get_all_records()

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


def consultar_oferta(nombre_programa=None, sede=None, modalidad=None):
    import os
    import json
    import gspread
    from google.oauth2.service_account import Credentials

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    try:
        raw_creds = os.getenv("GOOGLE_CREDS_JSON")
        if not raw_creds:
            return {"error": "No se encontraron credenciales en la variable de entorno."}

        creds_dict = json.loads(raw_creds)
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        client = gspread.authorize(creds)

        sheet = client.open("Copia de 2025 CONSOLIDADO MATRÍCULAS POSTGRADOS CHILE").worksheet("Oferta 2025")
        data = sheet.get_all_records()

        resultados = []

        # Normalizamos los filtros para hacer búsquedas case insensitive y sin espacios extras
        filtro_nombre = nombre_programa.lower().strip() if nombre_programa else None
        filtro_sede = sede.lower().strip() if sede else None
        filtro_modalidad = modalidad.lower().strip() if modalidad else None

        for fila in data:
            nombre = fila.get("Nombre de los programas", "").lower().strip()
            sede_actual = fila.get("Sede", "").lower().strip()
            modalidad_actual = fila.get("MODALIDAD", "").lower().strip()  # Fíjate que en tu hoja la columna es en mayúsculas

            if (not filtro_nombre or filtro_nombre in nombre) and \
               (not filtro_sede or filtro_sede in sede_actual) and \
               (not filtro_modalidad or filtro_modalidad in modalidad_actual):
                resultados.append({
                    "Programa": fila.get("PROGRAMAS", ""),
                    "Nombre de los programas": fila.get("Nombre de los programas", ""),
                    "Duración": fila.get("DURACIÓN", ""),
                    "Matrícula": fila.get("Matrícula", ""),
                    "Valores Arancel": fila.get("VALORES ARANCEL", ""),
                    "Modalidad": fila.get("MODALIDAD", ""),
                    "Sede": fila.get("Sede", ""),
                    "Categoría": fila.get("CATEGORÍA", ""),
                    "Año": fila.get("AÑO", ""),
                    "Estado": fila.get("ESTADO PARA VENTA", ""),
                    "Asesor 1": fila.get("ASESOR 1", ""),
                    # Puedes añadir más campos que quieras mostrar
                })

        if resultados:
            return {"programas": resultados}
        else:
            return {"programas": [], "mensaje": "No se encontraron programas que coincidan con los criterios."}

    except Exception as e:
        return {"error": f"Error al consultar la hoja Oferta 2025: {str(e)}"}
