!pip install tradingview_ta

from tradingview_ta import TA_Handler, Interval
import pandas as pd
import datetime

# Activos y mercado
activos = {
    "SPY": "AMEX",
    "DJI": "DJI",
    "NDX": "NASDAQ",
    "MSFT": "NASDAQ",
    "GOOGL": "NASDAQ",
    "META": "NASDAQ",
    "IBM": "NYSE",
    "V": "NYSE",
    "JPM": "NYSE",
    "MA": "NYSE",
    "AAPL": "NASDAQ",
    "AMD": "NASDAQ",
    "NVDA": "NASDAQ",
    "AMZN": "NASDAQ",
    "KO": "NYSE",
    "NKE": "NYSE",
    "DIS": "NYSE",
    "MCD": "NYSE",
    "NFLX": "NASDAQ",
    "CAT": "NYSE",
    "TSLA": "NASDAQ",
    "CVX": "NYSE",
    "XOM": "NYSE",
    "JNJ": "NYSE",
    "BTCUSD": "BINANCE",
    "ETHUSD": "BINANCE"
}

# Temporalidades
temporalidades = {
    "RSI_4H": Interval.INTERVAL_4_HOURS,
    "RSI_1D": Interval.INTERVAL_1_DAY,
    "RSI_1W": Interval.INTERVAL_1_WEEK,
    "RSI_1M": Interval.INTERVAL_1_MONTH
}

# Almacena resultados
data = []

for activo, mercado in activos.items():
    fila = {"Ticker": activo}
    for nombre_columna, intervalo in temporalidades.items():
        try:
            handler = TA_Handler(
                symbol=activo,
                exchange=mercado,
                screener="america",
                interval=intervalo
            )
            rsi_valor = handler.get_analysis().indicators.get("RSI")
            fila[nombre_columna] = rsi_valor
        except:
            fila[nombre_columna] = None
    data.append(fila)

# Crear DataFrame
df_rsi = pd.DataFrame(data)

# Convertir a numérico y redondear
for col in temporalidades.keys():
    df_rsi[col] = pd.to_numeric(df_rsi[col], errors="coerce").round(2)

# Filtro: RSI ≤ 30 o ≥ 70 en cualquiera de las temporalidades
df_filtrado = df_rsi[
    (df_rsi[["RSI_4H", "RSI_1D", "RSI_1W", "RSI_1M"]] <= 30).any(axis=1) |
    (df_rsi[["RSI_4H", "RSI_1D", "RSI_1W", "RSI_1M"]] >= 70).any(axis=1)
]

# Mostrar resultados
print(f"🕒 Actualizado: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
display(df_filtrado)
