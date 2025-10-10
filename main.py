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

# Obtener símbolos PERPETUAL USDT-margined
def get_futures_symbols():
    url = "https://fapi.binance.com/fapi/v1/exchangeInfo"
    try:
        info = requests.get(url, timeout=10).json()
        return [s["symbol"] for s in info["symbols"] if s["contractType"] == "PERPETUAL" and s["quoteAsset"] == "USDT"]
    except Exception as e:
        print(f"Error al obtener símbolos: {e}")
        return []

# Obtener volumen actual de 15m
def get_volume_15m(symbols, sleep_time=0.1):
    volumes = []
    for symbol in symbols:
        try:
            url = f"https://fapi.binance.com/fapi/v1/klines?symbol={symbol}&interval=15m&limit=1"
            response = requests.get(url, timeout=5)
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                volume = float(data[0][5])
                volumes.append((symbol, volume))
            else:
                print(f"{symbol}: respuesta vacía")
            time.sleep(sleep_time)
        except Exception as e:
            print(f"Error con {symbol}: {e}")
    return sorted(volumes, key=lambda x: x[1], reverse=True)

# Ejecutar flujo
symbols = get_futures_symbols()
top_volume = get_volume_15m(symbols)

# Escribir en Sheets
if top_volume:
    rows = [["Activo", "Volumen 15m"]] + [[s, round(v, 2)] for s, v in top_volume[:20]]
    sheet_top_volume.batch_clear(['A2:B'])
    sheet_top_volume.update('A1:B1', rows[0])
    sheet_top_volume.update(f'A2:B{len(rows)}', rows[1:])
    sheet_top_volume.update_cell(1, 4, f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("✅ Hoja actualizada correctamente.")
else:
    print("⚠️ No se obtuvo volumen para ningún activo.")


