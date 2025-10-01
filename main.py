import gspread
from tradingview_ta import TA_Handler, Interval
import json
import os
import time

# Reconstruir archivo JSON desde secreto
creds_json = os.environ['GOOGLE_SHEETS_CREDENTIALS']
with open('creds.json', 'w') as f:
    f.write(creds_json)

gc = gspread.service_account(filename='creds.json')
sheet = gc.open("Copia de Telegram Elite").worksheet("MA")

symbols = [
    "SPY", "QQQ", "MSFT", "GOOGL", "META", "IBM", "V", "JPM", "MA", "AAPL", "AMD", "NVDA", "AMZN", "KO", "DIS",
    "MCD", "NFLX", "CAT", "TSLA", "CVX", "XOM", "JNJ", "NKE"
]

def obtener_exchange(symbol):
    if symbol in {"SPY", "QQQ", "AAPL", "MSFT", "GOOGL", "META", "NVDA", "AMD", "AMZN", "NFLX", "TSLA"}:
        return "NASDAQ"
    else:
        return "NYSE"

# Encabezado
sheet.update('A1:B1', [["Activo", "Precio actual"]])

# Recolección
rows = []
for symbol in symbols:
    exchange = obtener_exchange(symbol)
    try:
        handler = TA_Handler(
            symbol=symbol,
            exchange=exchange,
            screener="america",
            interval=Interval.INTERVAL_4_HOURS
        )
        analysis = handler.get_analysis()
        precio = analysis.indicators.get("close")
        precio_final = round(precio, 2) if precio else "N/A"
        rows.append([symbol, precio_final])
    except Exception as e:
        print(f"Error en {symbol}: {e}")
        rows.append([symbol, "N/A"])
    time.sleep(0.5)

# Escribir desde A2
sheet.update('A2', rows)

