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

# Tu lista original (deduplicada y normalizada)
raw_symbols = list(set([
    "BNBUSDT", "BTCUSDT", "ETHUSDT", "WALUSDT", "SOLUSDT", "DOGEUSDT", "XRPUSDT", "LINKUSDT", "TAOUSDT", "PIVXUSDT",
    "DASHUSDT", "ZENUSDT", "SNXUSDT", "ALICEUSDT", "SCRTUSDT", "DUSKUSDT", "ZECUSDT", "MBLUSDT", "2ZUSDT", "OPENUSDT",
    "FFUSDT", "ASTERUSDT", "FETUSDT", "TSTUSDT", "MIRAUSDT", "UTKUSDT", "SOMIUSDT", "INUSDT", "ZORAUSDT", "SQDUSDT",
    "KGENUSDT", "BROCCOLIF3BUSDT", "AKEUSDT", "COAIUSDT", "NEARUSDT", "ETCUSDT", "FILUSDT", "WLDUSDT", "AXSUSDT",
    "MANAUSDT", "UNIUSDT", "OPUSDT", "DOTUSDT"
]))

# Paso 1: obtener lista de símbolos válidos en Binance Futures
def get_valid_futures_symbols():
    try:
        info = requests.get("https://fapi.binance.com/fapi/v1/exchangeInfo", timeout=10).json()
        return set(s["symbol"] for s in info["symbols"])
    except Exception as e:
        print(f"Error al obtener exchangeInfo: {e}")
        return set()

# Paso 2: consultar volumen solo para símbolos válidos
def get_volume_for_valid_symbols(symbols, valid_set, sleep_time=0.1):
    volumes = []
    for symbol in symbols:
        if symbol not in valid_set:
            print(f"{symbol} no existe en Binance Futures.")
            continue
        try:
            url = f"https://fapi.binance.com/fapi/v1/klines?symbol={symbol}&interval=15m&limit=1"
            response = requests.get(url, timeout=5)
            data = response.json()
            volume = float(data[0][5])
            print(f"{symbol}: {volume}")
            volumes.append((symbol, volume))
            time.sleep(sleep_time)
        except Exception as e:
            print(f"Error con {symbol}: {e}")
            continue
    return volumes

# Ejecutar flujo completo
valid_set = get_valid_futures_symbols()
top_volume = get_volume_for_valid_symbols(raw_symbols, valid_set)

if not top_volume:
    print("No se obtuvo volumen para ningún activo válido.")
else:
    rows = [["Activo", "Volumen 15m"]] + [[symbol, round(volume, 2)] for symbol, volume in top_volume]
    sheet_top_volume.batch_clear(['A2:B'])
    sheet_top_volume.update('A1:B1', [["Activo", "Volumen 15m"]])
    sheet_top_volume.update(f'A2:B{len(rows)}', rows[1:])
    sheet_top_volume.update_cell(1, 4, f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Hoja actualizada correctamente.")
