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
    "PAXGUSDT", "BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "BNBUSDT"
]

# Temporalidades corregidas
intervals = {
     "1H": Interval.INTERVAL_1_HOUR,
    "4H": Interval.INTERVAL_4_HOURS
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
sheet_rsi.batch_clear(['G2:I'])
sheet_rsi.update('G1:I1', [["Activo", "RSI 1H", "RSI 4H"]])
sheet_rsi.update(f'G2:I{len(rsi_map)+1}', rsi_map)

# Escribir Stoch
sheet_stoch.batch_clear(['G2:I'])
sheet_stoch.update('G1:I1', [["Activo", "Activo", "RSI 1H", "RSI 4H"]])
sheet_stoch.update(f'G2:I{len(stoch_map)+1}', stoch_map)

# Confluencias: mostrar todos los valores sin filtrar
sheet_confluencias.batch_clear(['G2:I'])
sheet_confluencias.update('G1:I1', [["Activo", "RSI 1H", "RSI 4H"]])

resultados = []
for i, symbol in enumerate(symbols):
    rsi_vals = rsi_map[i][1:]
    stoch_vals = stoch_map[i][1:]
    resultados.append([symbol] + rsi_vals + stoch_vals)

sheet_confluencias.update(f'G2:I{len(resultados)+1}', resultados)


