import requests
import time

# Lista fija de activos que tú proporcionaste (deduplicada y normalizada)
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
            print(f"{symbol}: {volume}")
            volumes.append((symbol, volume))
            time.sleep(sleep_time)
        except Exception as e:
            print(f"Error con {symbol}: {e}")
            continue
    return volumes

# Ejecutar verificación
get_volume_for_symbols(symbols)


