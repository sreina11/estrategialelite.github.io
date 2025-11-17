import gspread
from tradingview_ta import TA_Handler, Interval
import os

# === Reconstruir credenciales desde secreto ===
creds_json = os.environ['GOOGLE_SHEETS_CREDENTIALS']
with open('creds.json', 'w') as f:
    f.write(creds_json)

gc = gspread.service_account(filename='creds.json')
spreadsheet = gc.open("Copia de Telegram Elite")
sheet_rsi = spreadsheet.worksheet("RSI")
sheet_stoch = spreadsheet.worksheet("ST")

# === Lista de criptos (BINANCE) ===
symbols = [
    "PAXGUSDT", "BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "BNBUSDT"
]

# === Temporalidades ===
intervals = {
    "1H": Interval.INTERVAL_1_HOUR,
    "4H": Interval.INTERVAL_4_HOURS
}

# === RSI: recolectar datos 1H y 4H ===
rsi_map = []
for symbol in symbols:
    row = [symbol]
    for label, interval in intervals.items():
        try:
            handler = TA_Handler(
                symbol=symbol,
                exchange="BINANCE",
                screener="crypto",
                interval=interval
            )
            analysis = handler.get_analysis()
            rsi = analysis.indicators.get("RSI")
            row.append(round(rsi, 2) if rsi is not None else "N/A")
        except Exception as e:
            print(f"RSI error en {symbol} ({label}): {e}")
            row.append("N/A")
    rsi_map.append(row)

# === Stoch: recolectar datos 1H y 4H ===
stoch_map = []
for symbol in symbols:
    row = [symbol]
    for label, interval in intervals.items():
        try:
            handler = TA_Handler(
                symbol=symbol,
                exchange="BINANCE",
                screener="crypto",
                interval=interval
            )
            analysis = handler.get_analysis()
            stoch = analysis.indicators.get("Stoch.K")
            row.append(round(stoch, 2) if stoch is not None else "N/A")
        except Exception as e:
            print(f"Stoch error en {symbol} ({label}): {e}")
            row.append("N/A")
    stoch_map.append(row)

# === Escribir RSI en hoja "RSI" (G1:I) ===
sheet_rsi.batch_clear(['G2:I'])
sheet_rsi.update(values=[["Activo", "RSI 1H", "RSI 4H"]], range_name='G1:I1')
sheet_rsi.update(values=rsi_map, range_name=f'G2:I{len(rsi_map)+1}')

# === Escribir Stoch en hoja "ST" (G1:I) ===
sheet_stoch.batch_clear(['G2:I'])
sheet_stoch.update(values=[["Activo","Stoch 1H", "Stoch 4H"]], range_name='G1:I1')
sheet_stoch.update(values=stoch_map, range_name=f'G2:I{len(stoch_map)+1}')
