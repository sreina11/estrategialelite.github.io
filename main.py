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
sheet_rsi = gc.open("Copia de Telegram Elite").worksheet("RSI BIN")
sheet_stoch = gc.open("Copia de Telegram Elite").worksheet("STOC BIN")
sheet_confluencias = gc.open("Copia de Telegram Elite").worksheet("confluencias bin")

# Lista consolidada de criptos relevantes
symbols = [
     "EDENUSDT", "BROCCOLI714USDT", "WANUSDT", "OPENUSDT", "HEMIUSDT", "LISTAUSDT",
    "TSTUSDT", "MUBARAKUSDT", "FORMUSDT", "XPLUSDT"
]

# Temporalidades corregidas
intervals = {
    "5m": Interval.INTERVAL_5_MINUTES,
    "15m": Interval.INTERVAL_15_MINUTES
}

# RSI sin filtro
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

# Stoch sin filtro
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

# Escribir RSI
sheet_rsi.batch_clear(['A2:C'])
sheet_rsi.update('A1:C1', [["Activo", "RSI 5M", "RSI 15M"]])
sheet_rsi.update(f'A2:C{len(rsi_map)+1}', rsi_map)
sheet_rsi.update_cell(1, 5, f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Escribir Stoch
sheet_stoch.batch_clear(['A2:C'])
sheet_stoch.update('A1:C1', [["Activo", "Stoch 5M", "Stoch 15M"]])
sheet_stoch.update(f'A2:C{len(stoch_map)+1}', stoch_map)
sheet_stoch.update_cell(1, 5, f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Confluencias: mostrar todos los valores sin filtrar
sheet_confluencias.batch_clear(['A2:E'])
sheet_confluencias.update('A1:E1', [["Activo", "RSI 5M", "RSI 15M", "Stoch 5M", "Stoch 15M"]])

resultados = []
for i, symbol in enumerate(symbols):
    rsi_vals = rsi_map[i][1:]
    stoch_vals = stoch_map[i][1:]
    resultados.append([symbol] + rsi_vals + stoch_vals)

sheet_confluencias.update(f'A2:E{len(resultados)+1}', resultados)
sheet_confluencias.update_cell(1, 7, f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")



