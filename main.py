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
sheet = gc.open("Copia de Telegram Elite").worksheet("RSI")

# Lista de activos
symbols = [
    "SPY", ".DJI", ".INX", "MSFT", "GOOGL", "META", "IBM", "V", "JPM", "MA", "AAPL", "AMD", "NVDA", "AMZN", "KO", "DIS",
    "MCD", "NFLX", "CAT", "TSLA", "CVX", "XOM", "JNJ", "USDJPY", "USDCAD", "USDCHF", "USDAUD", "EURUSD", "EURJPY",
    "EURGBP", "EURAUD", "GBPUSD", "GBPJPY", "AUDUSD", "AUDJPY", "CADJPY", "CHFJPY", "CADCHF", "XAUUSD", "PAXGUSDT",
    "BTCUSD", "ETHUSD", "UKOIL", "XRPUSDT", "BNBUSDT", "SOLUSDT", "AVAXUSDT", "XLMUSDT", "LINKUSDT"
]

# Temporalidades
intervals = {
    "4H": Interval.INTERVAL_4_HOURS,
    "D": Interval.INTERVAL_1_DAY,
    "W": Interval.INTERVAL_1_WEEK
}

# Resultado final
filtered = []

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
                print(f"Error en {symbol} ({label}): {e}")
                row.append("N/A")

        if match:
            filtered.append(row)

    except Exception as e:
        print(f"Error general con {symbol}: {e}")

# Limpiar hoja y escribir resultados
sheet.batch_clear(['A2:D'])
sheet.update(range_name='A1:D1', values=[["Activo", "RSI 4H", "RSI Diario", "RSI Semanal"]])
sheet.update(range_name='A2', values=filtered)
sheet.update(range_name='E1', values=[[f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"]])





