import gspread
from tradingview_ta import TA_Handler, Interval
from datetime import datetime
import requests
from bs4 import BeautifulSoup
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
try:
    sheet_economicos = spreadsheet.worksheet("economicos")
except gspread.exceptions.WorksheetNotFound:
    sheet_economicos = spreadsheet.add_worksheet(title="economicos", rows="100", cols="10")

# === Activos válidos (FX + BTCUSD/ETHUSD) ===
symbols_fx = [
    "USDJPY", "AUDUSD", "EURUSD", "EURJPY", "EURGBP", "AUDJPY",
    "GBPUSD", "GBPJPY", "CADJPY", "CHFJPY", "CADCHF"
]
symbols_crypto_alias = ["BTCUSD", "ETHUSD", "PAXGUSD"]  # escrito tal cual en la hoja

intervals = {
    "1D": Interval.INTERVAL_1_DAY,
    "4H": Interval.INTERVAL_4_HOURS
}

# Exchanges candidatos para BTCUSD/ETHUSD (en orden de preferencia)
crypto_exchanges_fallback = ["OANDA", "BITSTAMP", "BITFINEX", "COINBASE"]

def get_indicator_with_fallback(symbol_alias, indicator_key, interval):
    """
    Intenta obtener un indicador para symbol_alias (p.ej. BTCUSD) probando exchanges candidatos.
    Devuelve float o 'N/A' si ninguno funciona. Mantiene el nombre escrito como BTCUSD/ETHUSD.
    """
    for ex in crypto_exchanges_fallback:
        try:
            handler = TA_Handler(
                symbol=symbol_alias,
                exchange=ex,
                screener="crypto",
                interval=interval
            )
            analysis = handler.get_analysis()
            val = analysis.indicators.get(indicator_key)
            if val is not None:
                return round(val, 2)
        except Exception as e:
            # Intento fallido, probamos el siguiente exchange
            continue
    return "N/A"

# === RSI ===
filtered_rsi = []

# FX (OANDA)
for symbol in symbols_fx:
    row = [symbol]
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
            row.append(round(rsi, 2) if rsi is not None else "N/A")
        except Exception as e:
            row.append("N/A")
    filtered_rsi.append(row)

# BTCUSD/ETHUSD con fallback de exchanges (nombre escrito tal cual)
for alias_symbol in symbols_crypto_alias:
    row = [alias_symbol]
    for label, interval in intervals.items():
        rsi_val = get_indicator_with_fallback(alias_symbol, "RSI", interval)
        row.append(rsi_val)
    filtered_rsi.append(row)

# === Estocástico ===
filtered_stoch = []

# FX (OANDA)
for symbol in symbols_fx:
    row = [symbol]
    for label, interval in intervals.items():
        try:
            handler = TA_Handler(
                symbol=symbol,
                exchange="OANDA",
                screener="forex",
                interval=interval
            )
            analysis = handler.get_analysis()
            stoch = analysis.indicators.get("Stoch.K")
            row.append(round(stoch, 2) if stoch is not None else "N/A")
        except Exception as e:
            row.append("N/A")
    filtered_stoch.append(row)

# BTCUSD/ETHUSD con fallback de exchanges (nombre escrito tal cual)
for alias_symbol in symbols_crypto_alias:
    row = [alias_symbol]
    for label, interval in intervals.items():
        stoch_val = get_indicator_with_fallback(alias_symbol, "Stoch.K", interval)
        row.append(stoch_val)
    filtered_stoch.append(row)

# === Escribir RSI ===
sheet_rsi.batch_clear(['A2:C'])
sheet_rsi.update('A1:C1', [["Activo", "RSI 1D", "RSI 4H"]])
sheet_rsi.update(f'A2:C{len(filtered_rsi)+1}', filtered_rsi)

# === Escribir Estocástico ===
sheet_stoch.batch_clear(['A2:C'])
sheet_stoch.update('A1:C1', [["Activo", "Stoch 1D", "Stoch 4H"]])
sheet_stoch.update(f'A2:C{len(filtered_stoch)+1}', filtered_stoch)

# === Indicadores económicos ===
indicadores = {
    "Tasa de Interés USA": "https://www.myfxbook.com/forex-economic-calendar/united-states/fed-interest-rate-decision",
    "PMI": "https://www.myfxbook.com/forex-economic-calendar/united-states/sp-global-manufacturing-pmi",
    "CPI": "https://www.myfxbook.com/forex-economic-calendar/united-states/inflation-rate-yoy",
    "PPI": "https://www.myfxbook.com/forex-economic-calendar/united-states/ppi-yoy",
    "Consumer Confidence": "https://www.myfxbook.com/forex-economic-calendar/united-states/cb-consumer-confidence",
    "Jobless Claims": "https://www.myfxbook.com/forex-economic-calendar/united-states/initial-jobless-claims",
    "Non-Farm Payroll": "https://www.myfxbook.com/forex-economic-calendar/united-states/non-farm-payrolls",
    "GDP": "https://www.myfxbook.com/forex-economic-calendar/united-states/gdp-growth-rate-qoq",
    "Industrial Production": "https://www.myfxbook.com/forex-economic-calendar/united-states/industrial-production-mom",
    "EUR Interest Rate": "https://www.myfxbook.com/forex-economic-calendar/euro-area/ecb-interest-rate-decision",
    "Japan Interest Rate": "https://www.myfxbook.com/forex-economic-calendar/japan/boj-interest-rate-decision",
    "England Interest Rate": "https://www.myfxbook.com/forex-economic-calendar/united-kingdom/boe-interest-rate-decision",
    "Australia Interest Rate": "https://www.myfxbook.com/forex-economic-calendar/australia/rba-interest-rate-decision"
}

selectores_css = {
    "Fecha": 'div:nth-child(3) > div > div:nth-child(3) > div:nth-child(2) > span:nth-child(2)',
    "Actual": 'div:nth-child(3) > div > div:nth-child(2) > div:nth-child(4) > span:nth-child(2) > span',
    "Esperado": 'div:nth-child(3) > div > div:nth-child(2) > div:nth-child(3) > span:nth-child(2)',
    "Anterior": 'div:nth-child(3) > div > div:nth-child(2) > div:nth-child(2) > span:nth-child(2) > span'
}

headers = {"User-Agent": "Mozilla/5.0"}
datos_economicos = []

for nombre, url in indicadores.items():
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        actual_raw = soup.select_one(selectores_css["Actual"])
        esperado_raw = soup.select_one(selectores_css["Esperado"])
        anterior_raw = soup.select_one(selectores_css["Anterior"])
        fecha_raw = soup.select_one(selectores_css["Fecha"])

        actual = actual_raw.text.strip() if actual_raw else "No disponible"
        esperado = esperado_raw.text.strip() if esperado_raw else "No disponible"
        anterior = anterior_raw.text.strip() if anterior_raw else "No disponible"
        fecha = fecha_raw.text.strip() if fecha_raw else "No disponible"

        datos_economicos.append([nombre, fecha, actual, esperado, anterior])

    except Exception as e:
        print(f"❌ Error en {nombre}: {e}")
        datos_economicos.append([nombre, "Error", "Error", "Error", "Error"])

# === Escribir hoja "economicos" ===
sheet_economicos.clear()
sheet_economicos.update("A1:E1", [["Indicador", "Fecha", "Actual", "Esperado", "Anterior"]])
sheet_economicos.update(f"A2:E{len(datos_economicos)+1}", datos_economicos)
sheet_economicos.update_cell(1, 7, f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

