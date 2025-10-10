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

# Obtener lista de símbolos válidos en Binance Futures
def get_futures_symbols():
    try:
        info = requests.get("https://fapi.binance.com/fapi/v1/exchangeInfo", timeout=10).json()
        return [s["symbol"] for s in info["symbols"] if s["contractType"] == "PERPETUAL" and s["quoteAsset"] == "USDT"]
    except Exception as e:
        print(f"Error al obtener exchangeInfo: {e}")
        return []

# Calcular incremento de volumen entre dos velas de 15m
def get_volume_increase(symbols, sleep_time=0.1):
    results = []
    for symbol in symbols:
        try:
            url = f"https://fapi.binance.com/fapi/v1/klines?symbol={symbol}&interval=15m&limit=2"
            response = requests.get(url, timeout=5)
            data = response.json()
            if isinstance(data, list) and len(data) == 2:
                vol_prev = float(data[0][5])
                vol_now = float(data[1][5])
                if vol_prev > 0:
                    change = ((vol_now - vol_prev) / vol_prev) * 100
                    results.append((symbol, round(change, 2), round(vol_now, 2)))
            time.sleep(sleep_time)
        except Exception as e:
            print(f"Error con {symbol}: {e}")
            continue
    return sorted(results, key=lambda x: x[1], reverse=True)

# Ejecutar flujo
symbols = get_futures_symbols()
top_changes = get_volume_increase(symbols)

# Escribir en Sheets
if top_changes:
    rows = [["Activo", "Cambio volumen %", "Volumen actual"]] + [[s, c, v] for s, c, v in top_changes[:20]]
    sheet_top_volume.batch_clear(['A2:C'])
    sheet_top_volume.update('A1:C1', rows[0])
    sheet_top_volume.update(f'A2:C{len(rows)}', rows[1:])
    sheet_top_volume.update_cell(1, 4, f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("✅ Hoja actualizada con incrementos de volumen.")
else:
    print("⚠️ No se detectaron incrementos de volumen.")


