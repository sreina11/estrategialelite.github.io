import gspread
from tradingview_ta import TA_Handler, Interval
from datetime import datetime
import json
import os
import time

# Reconstruir archivo JSON desde secreto
creds_json = os.environ['GOOGLE_SHEETS_CREDENTIALS']
with open('creds.json', 'w') as f:
    f.write(creds_json)

gc = gspread.service_account(filename='creds.json')
sheet_ma = gc.open("Copia de Telegram Elite").worksheet("MA")

symbols = [
    "SPY", "QQQ", "MSFT", "GOOGL", "META", "IBM", "V", "JPM", "MA", "AAPL", "AMD", "NVDA", "AMZN", "KO", "DIS",
    "MCD", "NFLX", "CAT", "TSLA", "CVX", "XOM", "JNJ", "NKE"
]

def obtener_exchange(symbol):
    if symbol in {"SPY", "QQQ", "AAPL", "MSFT", "GOOGL", "META", "NVDA", "AMD", "AMZN", "NFLX", "TSLA"}:
        return "NASDAQ"
    else:
        return "NYSE"

raw_data = []

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
        ma200 = analysis.moving_averages.get("MA200")

        print(f"{symbol} → Precio: {precio}, MA200: {ma200}")

        row = [
            symbol,
            round(precio, 2) if precio else "N/A",
            round(ma200["value"], 2) if ma200 else "N/A"
        ]
    except Exception as e:
        print(f"Error en {symbol}: {e}")
        row = [symbol, "N/A", "N/A"]

    raw_data.append(row)
    time.sleep(0.5)

# Escribir en hoja MA
sheet_ma.batch_clear(['A2:C'])
sheet_ma.update('A1:C1', [["Activo", "Precio 4H", "MA200 4H"]])
sheet_ma.update('A2', raw_data)
sheet_ma.update('E1', [[f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"]])



