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


