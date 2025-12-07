import gspread
from tradingview_ta import TA_Handler, Interval
from datetime import datetime
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
    "GOOGL": "NASDAQ", "META": "NASDAQ", "IBM": "NYSE", "V": "NYSE", "JPM": "NYSE", "MSFT": "NASDAQ",
    "MA": "NYSE", "AAPL": "NASDAQ", "AMD": "NASDAQ", "NVDA": "NASDAQ", "AMZN": "NASDAQ",
    "KO": "NYSE", "DIS": "NYSE", "MCD": "NYSE", "NFLX": "NASDAQ", "CAT": "NYSE",
    "TSLA": "NASDAQ", "XOM": "NYSE", "CVX": "NYSE", "JNJ": "NYSE",
    "SPY": "AMEX", "NDX": "NASDAQ": "OANDA"
}

intervals = {
    "1D": Interval.INTERVAL_1_DAY,
    "4H": Interval.INTERVAL_4_HOURS
}

# RSI de todos los símbolos
all_rsi = []
for symbol, exchange in symbols_info.items():
    row = [symbol]
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
            row.append(round(rsi, 2) if rsi is not None else "")
        except Exception as e:
            print(f"RSI error en {symbol} ({label}): {e}")
            row.append("")
    all_rsi.append(row)

# Estocástico de todos los símbolos
all_stoch = []
for symbol, exchange in symbols_info.items():
    row = [symbol]
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
            row.append(round(stoch, 2) if stoch is not None else "")
        except Exception as e:
            print(f"Stoch error en {symbol} ({label}): {e}")
            row.append("")
    all_stoch.append(row)

# Escribir RSI en A17:C
sheet_rsi.batch_clear(['A17:C'])
sheet_rsi.update(f'A17:C{16+len(all_rsi)}', all_rsi)

# Escribir Estocástico en A17:C
sheet_stoch.batch_clear(['A17:C'])
sheet_stoch.update(f'A17:C{16+len(all_stoch)}', all_stoch)
