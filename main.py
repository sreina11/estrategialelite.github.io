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

symbols = [
    "SPY", ".DJI", ".INX", "MSFT", "GOOGL", "META", "IBM", "V", "JPM", "MA", "AAPL", "AMD", "NVDA", "AMZN", "KO", "DIS",
    "MCD", "NFLX", "CAT", "TSLA", "CVX", "XOM", "JNJ", "USDJPY", "USDCAD", "USDCHF", "USDAUD", "EURUSD", "EURJPY",
    "EURGBP", "EURAUD", "GBPUSD", "GBPJPY", "AUDUSD", "AUDJPY", "CADJPY", "CHFJPY", "CADCHF", "XAUUSD", "PAXGUSDT",
    "BTCUSD", "ETHUSD", "UKOIL", "XRPUSDT", "BNBUSDT", "SOLUSDT", "AVAXUSDT", "XLMUSDT", "LINKUSDT"
]

intervals = {
    "4H": Interval.INTERVAL_4_HOURS,
    "D": Interval.INTERVAL_1_DAY,
    "W": Interval.INTERVAL_1_WEEK
}

# RSI
filtered_rsi = []

for symbol in symbols:
    try:
        row = [symbol]
        match = False

        for label, interval in intervals.items():
            try:
                handler = TA_Handler(
                    symbol=symbol,
                    exchange="BINANCE" if "USDT" in symbol else "NASDAQ",
                    screener="crypto" if "USDT" in symbol or "USD" in symbol else "america",
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

    except Exception as e:
        print(f"RSI error general con {symbol}: {e}")

# Estocástico
filtered_stoch = []

for symbol in symbols:
    try:
        row = [symbol]
        match = False

        for label, interval in intervals.items():
            try:
                handler = TA_Handler(
                    symbol=symbol,
                    exchange="BINANCE" if "USDT" in symbol else "NASDAQ",
                    screener="crypto" if "USDT" in symbol or "USD" in symbol else "america",
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

    except Exception as e:
        print(f"Stoch error general con {symbol}: {e}")

# Escribir RSI
sheet_rsi.batch_clear(['A2:D'])
sheet_rsi.update(range_name='A1:D1', values=[["Activo", "RSI 4H", "RSI Diario", "RSI Semanal"]])
sheet_rsi.update(range_name='A2', values=filtered_rsi)
sheet_rsi.update(range_name='E1', values=[[f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"]])

# Escribir Estocástico
sheet_stoch.batch_clear(['A2:D'])
sheet_stoch.update(range_name='A1:D1', values=[["Activo", "Stoch 4H", "Stoch Diario", "Stoch Semanal"]])
sheet_stoch.update(range_name='A2', values=filtered_stoch)
sheet_stoch.update(range_name='E1', values=[[f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"]])


def clasificar_activo(symbol):
    equity = {"SPY", ".DJI", ".INX", "MSFT", "GOOGL", "META", "IBM", "V", "JPM", "MA", "AAPL", "AMD", "NVDA", "AMZN", "KO", "DIS", "MCD", "NFLX", "CAT", "TSLA", "CVX", "XOM", "JNJ"}
    crypto = {"BTCUSD", "ETHUSD", "XRPUSDT", "BNBUSDT", "SOLUSDT", "AVAXUSDT", "XLMUSDT", "LINKUSDT", "PAXGUSDT"}
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
def dentro_del_rango(precio, media, tipo):
    if precio is None or media is None:
        return False, "N/A"
    delta = round((precio - media) / media * 100, 2)
    if tipo in ["equity", "crypto"]:
        return abs(delta) <= 1.0, f"{delta:+.2f}%"
    elif tipo in ["forex", "commodity"]:
        return abs(delta) <= 0.5, f"{delta:+.2f}%"
    return False, f"{delta:+.2f}%"

sheet_ma = gc.open("Copia de Telegram Elite").worksheet("MA")
sheet_bb = gc.open("Copia de Telegram Elite").worksheet("BB")

filtered_ma = []
filtered_bb = []

for symbol in symbols:
    tipo = clasificar_activo(symbol)
    try:
        row_ma = [symbol]
        row_bb = [symbol]
        match_ma = False

        for label, interval in intervals.items():
            try:
                handler = TA_Handler(
                    symbol=symbol,
                    exchange="BINANCE" if "USDT" in symbol else "NASDAQ",
                    screener="crypto" if "USDT" in symbol or "USD" in symbol else "america",
                    interval=interval
                )
                analysis = handler.get_analysis()
                precio = analysis.indicators.get("close")

                # MA
                for ma_key in ["MA20", "MA50", "MA200"]:
                    media = analysis.indicators.get(ma_key)
                    cumple, delta = dentro_del_rango(precio, media, tipo)
                    if cumple:
                        row_ma.append(f"{round(media,2)} ✅ ({delta})")
                        match_ma = True
                    else:
                        row_ma.append(f"{round(media,2)} ❌ ({delta})" if media else "N/A")

                # BB
                bb_upper = analysis.indicators.get("BB.upper")
                bb_lower = analysis.indicators.get("BB.lower")
                row_bb.append(round(bb_upper, 2) if bb_upper else "N/A")
                row_bb.append(round(bb_lower, 2) if bb_lower else "N/A")

            except Exception as e:
                print(f"MA/BB error en {symbol} ({label}): {e}")
                row_ma.extend(["N/A"] * 3)
                row_bb.extend(["N/A"] * 2)

        if match_ma:
            filtered_ma.append(row_ma)
        filtered_bb.append(row_bb)

    except Exception as e:
        print(f"MA/BB error general con {symbol}: {e}")
# MA
sheet_ma.batch_clear(['A2:Z'])
encabezado_ma = ["Activo"]
for label in intervals.keys():
    encabezado_ma.extend([f"MA20 {label}", f"MA50 {label}", f"MA200 {label}"])
sheet_ma.update(range_name='A1', values=[encabezado_ma])
sheet_ma.update(range_name='A2', values=filtered_ma)
sheet_ma.update(range_name='Z1', values=[[f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"]])

# BB
sheet_bb.batch_clear(['A2:Z'])
encabezado_bb = ["Activo"]
for label in intervals.keys():
    encabezado_bb.extend([f"BB Sup {label}", f"BB Inf {label}"])
sheet_bb.update(range_name='A1', values=[encabezado_bb])
sheet_bb.update(range_name='A2', values=filtered_bb)
sheet_bb.update(range_name='Z1', values=[[f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"]])
