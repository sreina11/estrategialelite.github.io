import gspread
from tradingview_ta import TA_Handler, Interval
from datetime import datetime
import json
import os

# Reconstruir archivo JSON desde secreto
creds_json = os.environ['GOOGLE_SHEETS_CREDENTIALS']
if not os.path.exists('creds.json'):
    with open('creds.json', 'w') as f:
        f.write(creds_json)

gc = gspread.service_account(filename='creds.json')
sheet_rsi = gc.open("Copia de Telegram Elite").worksheet("RSI")
sheet_stoch = gc.open("Copia de Telegram Elite").worksheet("ST")

# Símbolos con su exchange correcto
symbols_info = {
    "GOOGL": "NASDAQ", "META": "NASDAQ", "IBM": "NYSE", "V": "NYSE", "JPM": "NYSE",
    "MA": "NYSE", "AAPL": "NASDAQ", "AMD": "NASDAQ", "NVDA": "NASDAQ", "AMZN": "NASDAQ",
    "KO": "NYSE", "DIS": "NYSE", "MCD": "NYSE", "NFLX": "NASDAQ", "CAT": "NYSE",
    "TSLA": "NASDAQ", "XOM": "NYSE", "CVX": "NYSE", "JNJ": "NYSE",
    "SPY": "AMEX", "NDX": "NASDAQ", "US30": "OANDA"  # corregido para mayor compatibilidad
}

intervals = {
    "1H": Interval.INTERVAL_1_HOUR,
    "4H": Interval.INTERVAL_4_HOURS
}

# RSI filtrado
filtered_rsi = []

for symbol, exchange in symbols_info.items():
    row = [symbol]
    match = False
    for label, interval in intervals.items():
        try:
            handler = TA_Handler(
                symbol=symbol,
                exchange=exchange,
                screener="america" if exchange != "OANDA" else "forex",
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

# Estocástico filtrado
filtered_stoch = []

for symbol, exchange in symbols_info.items():
    row = [symbol]
    match = False
    for label, interval in intervals.items():
        try:
            handler = TA_Handler(
                symbol=symbol,
                exchange=exchange,
                screener="america" if exchange != "OANDA" else "forex",
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
sheet_rsi.batch_clear(['D2:F'])
sheet_rsi.update('D1:F1', [["Activo", "RSI 1H", "RSI 4H"]])
if filtered_rsi:
    sheet_rsi.update(f'A2:C{len(filtered_rsi)+1}', filtered_rsi)

# Escribir Estocástico
sheet_stoch.batch_clear(['D2:F'])
sheet_stoch.update('D1:F1', [["Activo", "Stoch 1H", "Stoch 4H"]])
if filtered_stoch:
    sheet_stoch.update(f'D2:F{len(filtered_stoch)+1}', filtered_stoch)

