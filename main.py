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

def get_top_futures_volume_15m(limit=20, sleep_time=0.1):
    """
    Consulta los contratos de futuros USDT en Binance con mayor volumen en los últimos 15 minutos.
    """
    try:
        info = requests.get("https://fapi.binance.com/fapi/v1/exchangeInfo", timeout=10).json()
        symbols = [s["symbol"] for s in info["symbols"] if s["contractType"] == "PERPETUAL" and s["quoteAsset"] == "USDT"]
    except Exception as e:
        print(f"Error al obtener símbolos de futuros: {e}")
        return []

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

    top = sorted(volumes, key=lambda x: x[1], reverse=True)[:limit]
    return top

# Obtener top volumen y preparar datos para Sheets
top_volume = get_top_futures_volume_15m(limit=20)
rows = [["Activo", "Volumen 15m"]] + [[symbol, round(volume, 2)] for symbol, volume in top_volume]

# Escribir en hoja "top volume"
sheet_top_volume.batch_clear(['A2:B'])
sheet_top_volume.update('A1:B1', [["Activo", "Volumen 15m"]])
sheet_top_volume.update(f'A2:B{len(rows)}', rows[1:])
sheet_top_volume.update_cell(1, 4, f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")



