import gspread
from tradingview_ta import TA_Handler, Interval
import json
import os
import time

# Reconstruir credenciales
creds_json = os.environ['GOOGLE_SHEETS_CREDENTIALS']
with open('creds.json', 'w') as f:
    f.write(creds_json)

gc = gspread.service_account(filename='creds.json')
sheet = gc.open("Copia de Telegram Elite").worksheet("MA")

# Lista completa de activos
symbols = [
    # Índices
    "SPX500", "DJI", "NAS100",
    # Acciones
    "SPY", "MSFT", "GOOGL", "META", "IBM", "V", "JPM", "MA", "AAPL", "AMD", "NVDA", "AMZN", "KO", "DIS",
    "MCD", "NFLX", "CAT", "TSLA", "CVX", "XOM", "JNJ",
    # Forex
    "USDJPY", "USDCAD", "USDCHF", "USDAUD", "EURUSD", "EURJPY", "EURGBP", "EURAUD", "GBPUSD", "GBPJPY",
    "AUDUSD", "AUDJPY", "CADJPY", "CHFJPY", "CADCHF",
    # Cripto
    "BTCUSD", "ETHUSD", "XRPUSDT", "BNBUSDT", "SOLUSDT", "AVAXUSDT", "XLMUSDT", "LINKUSDT", "PAXGUSDT",
    # Commodities
    "XAUUSD", "UKOIL"
]

def obtener_exchange(symbol):
    if symbol in {"BTCUSD", "ETHUSD", "XRPUSDT", "BNBUSDT", "SOLUSDT", "AVAXUSDT", "XLMUSDT", "LINKUSDT", "PAXGUSDT"}:
        return "BINANCE"
    elif symbol in {"SPY", "AAPL", "MSFT", "GOOGL", "META", "NVDA", "AMD", "AMZN", "NFLX", "TSLA"}:
        return "NASDAQ"
    elif symbol in {"CVX", "XOM", "KO", "DIS", "MCD", "IBM", "V", "JPM", "MA", "CAT", "JNJ"}:
        return "NYSE"
    elif symbol in {"UKOIL", "SPX500", "DJI", "NAS100"}:
        return "TVC"
    elif symbol in {"XAUUSD", "EURUSD", "USDJPY", "GBPUSD", "USDCAD", "USDCHF", "AUDUSD", "NZDUSD",
                    "EURJPY", "EURGBP", "EURAUD", "GBPJPY", "AUDJPY", "CADJPY", "CHFJPY", "CADCHF", "USDAUD"}:
        return "OANDA"
    else:
        return "BINANCE"

def obtener_screener(symbol):
    if symbol in {"BTCUSD", "ETHUSD", "XRPUSDT", "BNBUSDT", "SOLUSDT", "AVAXUSDT", "XLMUSDT", "LINKUSDT", "PAXGUSDT"}:
        return "crypto"
    elif symbol in {"USDJPY", "USDCAD", "USDCHF", "USDAUD", "EURUSD", "EURJPY", "EURGBP", "EURAUD", "GBPUSD", "GBPJPY",
                    "AUDUSD", "AUDJPY", "CADJPY", "CHFJPY", "CADCHF", "XAUUSD", "UKOIL"}:
        return "forex"
    elif symbol in {"SPX500", "DJI", "NAS100"}:
        return "indices"
    else:
        return "america"

# Encabezado
sheet.update('A1:C1', [["Activo", "Precio actual", "Estado"]])

# Recolección
rows = []
for symbol in symbols:
    exchange = obtener_exchange(symbol)
    screener = obtener_screener(symbol)
    try:
        handler = TA_Handler(
            symbol=symbol,
            exchange=exchange,
            screener=screener,
            interval=Interval.INTERVAL_4_HOURS
        )
        analysis = handler.get_analysis()
        precio = analysis.indicators.get("close")
        if precio is not None:
            precio_final = round(precio, 2)
            estado = "OK"
        else:
            precio_final = "N/A"
            estado = "Error: precio vacío"
    except Exception as e:
        precio_final = "N/A"
        estado = f"Error: {str(e).splitlines()[0]}"
    rows.append([symbol, precio_final, estado])
    time.sleep(0.5)

# Escribir en hoja
sheet.update('A2', rows)

