import gspread
from tradingview_ta import TA_Handler, Interval
from datetime import datetime
import os

# === Reconstruir credenciales ===
creds_json = os.environ['GOOGLE_SHEETS_CREDENTIALS']
if not os.path.exists('creds.json'):
    with open('creds.json', 'w') as f:
        f.write(creds_json)

gc = gspread.service_account(filename='creds.json')
spreadsheet = gc.open("Copia de Telegram Elite")
sheet_rsi = spreadsheet.worksheet("RSI")
sheet_stoch = spreadsheet.worksheet("ST")

# === Activos (FX + BTC/ETH) ===
symbols_fx = [
    "USDJPY", "AUDUSD", "EURUSD", "EURJPY", "EURGBP", "AUDJPY",
    "GBPUSD", "GBPJPY", "CADJPY", "CHFJPY", "CADCHF"
]

symbols_crypto = ["BTCUSD", "ETHUSD"]

intervals = {
    "1D": Interval.INTERVAL_1_DAY,
    "4H": Interval.INTERVAL_4_HOURS
}

# Exchanges para Crypto Fallback
crypto_exchanges_fallback = ["OANDA", "BITSTAMP", "BITFINEX", "COINBASE"]

def get_crypto_indicator(symbol, indicator_key, interval):
    """ Intenta obtener indicador de crypto con fallback de exchanges """
    for ex in crypto_exchanges_fallback:
        try:
            handler = TA_Handler(
                symbol=symbol,
                exchange=ex,
                screener="crypto",
                interval=interval
            )
            analysis = handler.get_analysis()
            val = analysis.indicators.get(indicator_key)
            if val is not None:
                return round(val, 2)
        except:
            continue
    return "N/A"

# === Procesamiento ===
filtered_rsi = []
filtered_stoch = []

# 1. Procesar FX (OANDA)
for symbol in symbols_fx:
    row_rsi = [symbol]
    row_stoch = [symbol]
    for label, interval in intervals.items():
        try:
            handler = TA_Handler(
                symbol=symbol,
                exchange="OANDA",
                screener="forex",
                interval=interval
            )
            analysis = handler.get_analysis()
            rsi = analysis.indicators.get("RSI")
            st = analysis.indicators.get("Stoch.K")
            row_rsi.append(round(rsi, 2) if rsi is not None else "N/A")
            row_stoch.append(round(st, 2) if st is not None else "N/A")
        except:
            row_rsi.append("N/A")
            row_stoch.append("N/A")
    filtered_rsi.append(row_rsi)
    filtered_stoch.append(row_stoch)

# 2. Procesar Crypto (BTC/ETH)
for symbol in symbols_crypto:
    row_rsi = [symbol]
    row_stoch = [symbol]
    for label, interval in intervals.items():
        row_rsi.append(get_crypto_indicator(symbol, "RSI", interval))
        row_stoch.append(get_crypto_indicator(symbol, "Stoch.K", interval))
    filtered_rsi.append(row_rsi)
    filtered_stoch.append(row_stoch)

# === Escritura en Sheets ===

# Limpiar y actualizar RSI
sheet_rsi.batch_clear(['A2:C20'])
sheet_rsi.update('A1:C1', [["Activo", "RSI 1D", "RSI 4H"]])
sheet_rsi.update(f'A2:C{len(filtered_rsi)+1}', filtered_rsi)

# Limpiar y actualizar Estocástico
sheet_stoch.batch_clear(['A2:C20'])
sheet_stoch.update('A1:C1', [["Activo", "Stoch 1D", "Stoch 4H"]])
sheet_stoch.update(f'A2:C{len(filtered_stoch)+1}', filtered_stoch)

# Marca de tiempo de control
sheet_rsi.update_cell(1, 5, f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

print("✅ Código simplificado: Se eliminaron económicos y activos extra.")
