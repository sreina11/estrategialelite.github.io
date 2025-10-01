import gspread
from tradingview_ta import TA_Handler, Interval
import json
import os

# Reconstruir archivo JSON desde secreto
creds_json = os.environ['GOOGLE_SHEETS_CREDENTIALS']
with open('creds.json', 'w') as f:
    f.write(creds_json)

gc = gspread.service_account(filename='creds.json')
sheet = gc.open("Copia de Telegram Elite").worksheet("MA")

# Activo único
symbol = "AAPL"
exchange = "NASDAQ"

# Obtener precio actual en 4H
handler = TA_Handler(
    symbol=symbol,
    exchange=exchange,
    screener="america",
    interval=Interval.INTERVAL_4_HOURS
)

analysis = handler.get_analysis()
precio = analysis.indicators.get("close")
precio_final = round(precio, 2) if precio else "N/A"

# Escribir en hoja
sheet.update('A1', [[symbol]])
sheet.update('B2', [[precio_final]])


