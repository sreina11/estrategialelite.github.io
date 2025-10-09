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
    "AIAUSDT", "4USDT", "GIGGLEUSDT", "币安人生USDT", "BLESSUSDT", "STBLUSDT", "DORAUSDT",
    "LISTAUSDT", "XANUSDT", "FORMUSDT", "DEXEUSDT", "NMDUSDT", "CAKEUSDT", "ASTERUSDT",
    "WKCUSDT", "MYXUSDT", "XVSUSDT", "SIRENUSDT", "MOGUSDT", "TWTUSDT", "PTBUSDT"
]


# Temporalidades corregidas
intervals = {
    "5m": Interval.INTERVAL_5_MINUTES,
    "15m": Interval.INTERVAL_15_MINUTES
}

# RSI filtrado
filtered_rsi = []
rsi_map = {}

for symbol in symbols:
    row = [symbol]
    match = False
    values = []

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

            if rsi is not None:
                rsi_val = round(rsi, 2)
                values.append(rsi_val)
                row.append(rsi_val)
                if rsi_val <= 30 or rsi_val >= 70:
                    match = True
            else:
                values.append("N/A")
                row.append("N/A")

        except Exception as e:
            print(f"RSI error en {symbol} ({label}): {e}")
            values.append("N/A")
            row.append("N/A")

    if match:
        filtered_rsi.append(row)
    rsi_map[symbol] = values

# Stoch filtrado
filtered_stoch = []
stoch_map = {}

for symbol in symbols:
    row = [symbol]
    match = False
    values = []

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

            if stoch is not None:
                stoch_val = round(stoch, 2)
                values.append(stoch_val)
                row.append(stoch_val)
                if stoch_val <= 20 or stoch_val >= 80:
                    match = True
            else:
                values.append("N/A")
                row.append("N/A")

        except Exception as e:
            print(f"Stoch error en {symbol} ({label}): {e}")
            values.append("N/A")
            row.append("N/A")

    if match:
        filtered_stoch.append(row)
    stoch_map[symbol] = values

# Escribir RSI
sheet_rsi.batch_clear(['A2:C'])
sheet_rsi.update('A1:C1', [["Activo", "RSI 5M", "RSI 15M"]])
if filtered_rsi:
    sheet_rsi.update(f'A2:C{len(filtered_rsi)+1}', filtered_rsi)
sheet_rsi.update_cell(1, 5, f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Escribir Stoch
sheet_stoch.batch_clear(['A2:C'])
sheet_stoch.update('A1:C1', [["Activo", "Stoch 5M", "Stoch 15M"]])
if filtered_stoch:
    sheet_stoch.update(f'A2:C{len(filtered_stoch)+1}', filtered_stoch)
sheet_stoch.update_cell(1, 5, f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Detectar confluencias
sheet_confluencias.batch_clear(['A2:E'])
sheet_confluencias.update('A1:E1', [["Activo", "RSI 5M", "RSI 15M", "Stoch 5M", "Stoch 15M"]])

resultados = []

for symbol in symbols:
    if symbol not in rsi_map or symbol not in stoch_map:
        continue

    rsi_vals = rsi_map[symbol]
    stoch_vals = stoch_map[symbol]

    rsi_extrema = any(val != "N/A" and (val <= 30 or val >= 70) for val in rsi_vals)
    stoch_extrema = any(val != "N/A" and (val <= 20 or val >= 80) for val in stoch_vals)

    if rsi_extrema and stoch_extrema:
        resultados.append([symbol] + rsi_vals + stoch_vals)

if resultados:
    sheet_confluencias.update(f'A2:E{len(resultados)+1}', [row[:5] for row in resultados])
    sheet_confluencias.update_cell(1, 7, f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")



