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
    "SPY", ".DJI", ".INX", "MSFT", "GOOGL", "META", "IBM", "V", "JPM", "MA", "AAPL", "AMD", "NVDA", "AMZN", "KO", "DIS",
    "MCD", "NFLX", "CAT", "TSLA", "CVX", "XOM", "JNJ", "USDJPY", "USDCAD", "USDCHF", "USDAUD", "EURUSD", "EURJPY",
    "EURGBP", "EURAUD", "GBPUSD", "GBPJPY", "AUDUSD", "AUDJPY", "CADJPY", "CHFJPY", "CADCHF", "XAUUSD", "BTCUSD",
    "ETHUSD", "UKOIL", "XRPUSDT", "BNBUSDT", "SOLUSDT", "AVAXUSDT", "XLMUSDT", "LINKUSDT"
]

intervals = {
    "4H": Interval.INTERVAL_4_HOURS,
    "D": Interval.INTERVAL_1_DAY,
    "W": Interval.INTERVAL_1_WEEK,
    "M": Interval.INTERVAL_1_MONTH
}

def obtener_exchange(symbol):
    if symbol.endswith("USDT") or symbol in {"BTCUSD", "ETHUSD", "XRPUSDT", "BNBUSDT", "SOLUSDT", "AVAXUSDT", "XLMUSDT", "LINKUSDT"}:
        return "BINANCE"
    elif symbol in {"SPY", "AAPL", "MSFT", "GOOGL", "META", "NVDA", "AMD", "AMZN", "NFLX", "TSLA"}:
        return "NASDAQ"
    elif symbol in {"CVX", "XOM", "KO", "DIS", "MCD", "IBM", "V", "JPM", "MA", "CAT"}:
        return "NYSE"
    elif symbol in {"UKOIL"}:
        return "TVC"
    elif symbol in {"XAUUSD", "EURUSD", "USDJPY", "GBPUSD", "USDCAD", "USDCHF", "AUDUSD", "NZDUSD"}:
        return "OANDA"
    else:
        return "BINANCE"

# Recolección cruda
raw_ma = []

for symbol in symbols:
    exchange = obtener_exchange(symbol)
    row = [symbol]

    for label, interval in intervals.items():
        try:
            handler = TA_Handler(
                symbol=symbol,
                exchange=exchange,
                screener="crypto" if "USDT" in symbol or "USD" in symbol else "america",
                interval=interval
            )
            analysis = handler.get_analysis()
            precio = analysis.indicators.get("close")
            ma20 = analysis.indicators.get("MA20")
            ma50 = analysis.indicators.get("MA50")
            ma200 = analysis.indicators.get("MA200")

            row.extend([
                round(precio, 2) if precio else "N/A",
                round(ma20, 2) if ma20 else "N/A",
                round(ma50, 2) if ma50 else "N/A",
                round(ma200, 2) if ma200 else "N/A"
            ])

        except Exception as e:
            print(f"Error en {symbol} ({label}): {e}")
            row.extend(["N/A"] * 4)

    raw_ma.append(row)
    time.sleep(0.5)

# Escribir en hoja MA
sheet_ma.batch_clear(['A2:Z'])
encabezado = ["Activo"]
for label in intervals.keys():
    encabezado.extend([f"Precio {label}", f"MA20 {label}", f"MA50 {label}", f"MA200 {label}"])
sheet_ma.update('A1', [encabezado])
sheet_ma.update('A2', raw_ma)
sheet_ma.update('F1', [[f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"]])

