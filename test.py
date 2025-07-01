import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", scope)
client = gspread.authorize(creds)

# Cambia los nombres si es necesario
spreadsheet_name = "Copia de 2025 CONSOLIDADO MATRÍCULAS POSTGRADOS CHILE"
worksheet_name = "MATRÍCULAS CHILE"

sheet = client.open(spreadsheet_name).worksheet(worksheet_name)
data = sheet.get_all_records()

# Imprime la primera fila como test
print("✅ Conexión exitosa. Primer registro:")
print(data[0])
