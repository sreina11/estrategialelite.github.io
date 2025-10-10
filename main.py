import requests
import gspread
import os
import time
from datetime import datetime

# Reconstruir archivo JSON desde secreto
creds_json = os.environ['GOOGLE_SHEETS_CREDENTIALS']
with open('creds.json', 'w') as f:
    f.write(creds_json)

gc = gspread.service_account(filename='creds.json')
sheet_top_volume = gc.open("Copia de Telegram Elite").worksheet("top volume")

# Lista personalizada de activos (deduplicada y normalizada)
symbols = list(set([
    "BNBUSDT", "BTCUSDT", "ETHUSDT", "WALUSDT", "SOLUSDT", "DOGEUSDT", "XRPUSDT", "LINKUSDT", "TAOUSDT", "PIVXUSDT",
    "DASHUSDT", "ZENUSDT", "SNXUSDT", "ALICEUSDT", "DUSKUSDT", "SCRTUSDT", "ROSEUSDT", "2ZUSDT", "MBLUSDT", "OPENUSDT",
    "STOUSDT", "FFUSDT", "TSTUSDT", "ASTERUSDT", "FETUSDT", "MIRAUSDT", "FORMUSDT", "LTCUSDT", "ZECUSDT", "INUSDT",
    "ZORAUSDT", "KGENUSDT", "SQDUSDT", "BROCCOLIF3BUSDT", "AKEUSDT", "COAIUSDT", "NEARUSDT", "ETCUSDT", "WLDUSDT",
    "FILUSDT", "AXSUSDT", "MANAUSDT", "UNIUSDT", "DOTUSDT", "OPUSDT"
]))

def get_volume_for_symbols(symbols, sleep_time=0.1):
    volumes = []
    for symbol in symbols:
        try:
            url = f"https://fapi.binance.com/fapi/v1/klines?symbol={symbol}&interval=15m&limit=1"
            response = requests.get(url, timeout=5)
            data = response.json()
            volume = float(data[0][5])
            volumes.append((symbol, volume))
            time.sleep(sleep_time)
        except Exception as e:
            print(f"Error con {symbol}: {e}")
            continue
    return volumes

# Obtener volumen y preparar datos para Sheets
top_volume = get_volume_for_symbols(symbols)
if not top_volume:
    print("No se obtuvo volumen para ningún activo.")
else:
    rows = [["Activo", "Volumen 15m"]] + [[symbol, round(volume, 2)] for symbol, volume in top_volume]

    # Escribir en hoja "top volume"
    sheet_top_volume.batch_clear(['A2:B'])
    sheet_top_volume.update('A1:B1', [["Activo", "Volumen 15m"]])
    sheet_top_volume.update(f'A2:B{len(rows)}', rows[1:])
    sheet_top_volume.update_cell(1, 4, f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    print("Hoja actualizada correctamente.")



