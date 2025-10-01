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

def clasificar_activo(symbol):
    equity = {"SPY", ".DJI", ".INX", "MSFT", "GOOGL", "META", "IBM", "V", "JPM", "MA", "AAPL", "AMD", "NVDA", "AMZN", "KO", "DIS", "MCD", "NFLX", "CAT", "TSLA", "CVX", "XOM", "JNJ"}
    crypto = {"BTCUSD", "ETHUSD", "XRPUSDT", "BNBUSDT", "SOLUSDT", "AVAXUSDT", "XLMUSDT", "LINKUSDT"}
    forex = {"USDJPY", "USDCAD", "USDCHF", "USDAUD", "EURUSD", "EURJPY", "EURGBP", "EURAUD", "GBPUSD", "GBPJPY", "AUDUSD", "AUDJPY", "CADJPY", "CHFJPY", "CADCHF"}
    commodity = {"XAUUSD", "UKOIL"}

    if symbol in equity:
        return "equity"
    elif symbol in crypto:
        return "crypto"
    elif symbol in forex:
        return "forex"
    elif symbol in commodity:
        return "commodity"
    else:
        return "unknown"

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

def dentro_del_rango(precio, media, tipo):
    if precio is None or media is None:
        return False, "N/A"
    delta = round((precio - media) / media * 100, 2)
    if tipo in ["equity", "crypto"]:
        return abs(delta) <= 1.0, f"{delta:+.2f}%"
    elif tipo in ["forex", "commodity"]:
        return abs(delta) <= 0.5, f"{delta:+.2f}%"
    return False, f"{delta:+.2f}%"

# MA
filtered_ma = []

for symbol in symbols:
    tipo = clasificar_activo(symbol)
    exchange = obtener_exchange(symbol)
    try:
        row = [symbol]
        match = False

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

                for ma_key in ["MA20", "MA50", "MA200"]:
                    media = analysis.indicators.get(ma_key)
                    cumple, delta = dentro_del_rango(precio, media, tipo)
                    if cumple:
                        row.append(f"{round(media,2)} ✅ ({delta})")
                        match = True
                    else:
                        row.append(f"{round(media,2)} ❌ ({delta})" if media else "N/A")

            except Exception as e:
                print(f"MA error en {symbol} ({label}): {e}")
                row.extend(["N/A"] * 3)

        if match:
            filtered_ma.append(row)

    except Exception as e:
        print(f"MA error general con {symbol}: {e}")
    time.sleep(0.5)

# Escribir MA
sheet_ma.batch_clear(['A2:Z'])
encabezado = ["Activo"]
for label in intervals.keys():
    encabezado.extend([f"MA20 {label}", f"MA50 {label}", f"MA200 {label}"])
sheet_ma.update('A1', [encabezado])
sheet_ma.update('A2', filtered_ma)
sheet_ma.update('F1', [[f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"]])



