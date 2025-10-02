import gspread
from tradingview_ta import TA_Handler, Interval
from datetime import datetime
import json
import os

# Reconstruir archivo JSON desde secreto
creds_json = os.environ['GOOGLE_SHEETS_CREDENTIALS']
with open('creds.json', 'w') as f:
    f.write(creds_json)

gc = gspread.service_account(filename='creds.json')
sheet_rsi = gc.open("Copia de Telegram Elite").worksheet("RSI")
sheet_stoch = gc.open("Copia de Telegram Elite").worksheet("ST")

# Activos: Forex y Commodities
symbols = [
    "USDJPY", "USDCAD", "USDCHF", "USDAUD", "EURUSD", "EURJPY", "EURGBP", "EURAUD",
    "GBPUSD", "GBPJPY", "AUDUSD", "AUDJPY", "CADJPY", "CHFJPY", "CADCHF",
    "XAUUSD", "UKOIL", "USOIL", "XAGUSD"
]

intervals = {
    "1H": Interval.INTERVAL_1_HOUR,
    "4H": Interval.INTERVAL_4_HOURS
}

# RSI
filtered_rsi = []

for symbol in symbols:
    row = [symbol]
    match = False

    for label, interval in intervals.items():
        try:
            handler = TA_Handler(
                symbol=symbol,
                exchange="OANDA",
                screener="forex",
                interval=interval
            )
            analysis = handler.get_analysis()
            rsi = analysis.indicators.get("RSI")

            if rsi is not None:
                row.append(round(rsi, 2))
                if rsi <= 30 or rsi >= 70:
                    match = True
            else:
                row.append("N/A")

        except Exception as e:
            print(f"RSI error en {symbol} ({label}): {e}")
            row.append("N/A")

    if match:
        filtered_rsi.append(row)

# Estocástico
filtered_stoch = []

for symbol in symbols:
    row = [symbol]
    match = False

    for label, interval in intervals.items():
        try:
            handler = TA_Handler(
                symbol=symbol,
                exchange="OANDA",
                screener="forex",
                interval=interval
            )
            analysis = handler.get_analysis()
            stoch = analysis.indicators.get("Stoch.K")

            if stoch is not None:
                row.append(round(stoch, 2))
                if stoch <= 20 or stoch >= 80:
                    match = True
            else:
                row.append("N/A")

        except Exception as e:
            print(f"Stoch error en {symbol} ({label}): {e}")
            row.append("N/A")

    if match:
        filtered_stoch.append(row)

# Escribir RSI
sheet_rsi.batch_clear(['A2:C'])
sheet_rsi.update('A1:C1', [["Activo", "RSI 1H", "RSI 4H"]])
if filtered_rsi:
    sheet_rsi.update(f'A2:C{len(filtered_rsi)+1}', filtered_rsi)
    sheet_rsi.format(f'A2:C{len(filtered_rsi)+1}', {
        "textFormat": {"foregroundColor": {"red": 0, "green": 0, "blue": 0}}
    })
sheet_rsi.update_cell(1, 5, f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Escribir Estocástico
sheet_stoch.batch_clear(['A2:C'])
sheet_stoch.update('A1:C1', [["Activo", "Stoch 1H", "Stoch 4H"]])
if filtered_stoch:
    sheet_stoch.update(f'A2:C{len(filtered_stoch)+1}', filtered_stoch)
    sheet_stoch.format(f'A2:C{len(filtered_stoch)+1}', {
        "textFormat": {"foregroundColor": {"red": 0, "green": 0, "blue": 0}}
    })
sheet_stoch.update_cell(1, 5, f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


