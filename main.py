import gspread
from tradingview_ta import TA_Handler, Interval, Exchange
from datetime import datetime
import json
import os

# Reconstruir archivo JSON desde secreto
creds_json = os.environ['GOOGLE_SHEETS_CREDENTIALS']
with open('creds.json', 'w') as f:
    f.write(creds_json)

gc = gspread.service_account(filename='creds.json')
sheet = gc.open("Nombre de tu hoja").worksheet("RSI")  # Cambia el nombre si es necesario

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
        handler = TA_Handler(
            symbol=symbol,
            exchange="BINANCE" if "USDT" in symbol else "NASDAQ",
            screener="crypto" if "USDT" in symbol or "USD" in symbol else "america",
            interval=Interval.INTERVAL_1_DAY  # Temporalidad inicial, se sobreescribe abajo
        )

        row = [symbol]
        match = False

        for label, interval in intervals.items():
            handler.set_interval(interval)
            analysis = handler.get_analysis()
            rsi = analysis.indicators.get("RSI")

            if rsi is not None:
                row.append(round(rsi, 2))
                if rsi <= 30 or rsi >= 70:
                    match = True
            else:
                row.append("N/A")

        if match:
            filtered.append(row)

    except Exception as e:
        print(f"Error con {symbol}: {e}")

# Limpiar hoja y escribir resultados
sheet.batch_clear(['A2:D'])
sheet.update('A1:D1', [["Activo", "RSI 4H", "RSI Diario", "RSI Semanal"]])
sheet.update(f"A2", filtered)
sheet.update('E1', f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")



