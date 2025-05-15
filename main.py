# RSI. Activos y mercado
from tradingview_ta import TA_Handler, Interval
import pandas as pd
import datetime

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
print(df_filtrado)

import requests
import datetime
import pandas as pd

import requests
import datetime
import pandas as pd
import os  # Importar para manejar variables de entorno

# ⚠️ **Reemplaza el ID con el que obtuviste en la publicación inicial**
post_id = "1002"  # ⚠️ Usa el ID correcto generado antes

# URL de la API para actualizar el post
wordpress_url = f"https://estrategiaelite.com/wp-json/wp/v2/posts/{post_id}"

# **Aplicar colores al DataFrame**
def aplicar_colores(valor):
    """Aplica colores y negrita basados en el valor de RSI."""
    if valor >= 70:
        return f'<span style="color: red; font-weight: bold;">{valor}</span>'  # Sobrecompra
    elif valor <= 30:
        return f'<span style="color: green; font-weight: bold;">{valor}</span>'  # Sobreventa
    else:
        return f'<span style="font-weight: bold;">{valor}</span>'  # Negrita sin color


# **Copiar `df_filtrado` para aplicar colores**
df_coloreado = df_filtrado.copy()

# **Aplicar la función a las columnas RSI**
for col in ["RSI_4H", "RSI_1D", "RSI_1W", "RSI_1M"]:
    df_coloreado[col] = df_coloreado[col].apply(aplicar_colores)

# **Diseño de la tabla en HTML con estilos**
def generar_tabla_html(df):
    estilos = """
    <style>
        table {border-collapse: collapse; width: 100%; font-family: Arial;}
        th, td {border: 1px solid #ddd; padding: 10px; text-align: center;}
        th {background-color: #0073aa; color: white; font-weight: bold;}
        tr:nth-child(even) {background-color: #f2f2f2;}
        tr:hover {background-color: #ddd;}
    </style>
    """
    return estilos + df.to_html(index=False, escape=False)

# **Datos de la actualización**
post_data = {
    "title": f"Índice RSI - Actualización {datetime.datetime.now().strftime('%Y-%m-%d')}",
    "content": generar_tabla_html(df_coloreado)
}

# **Ejecutar la solicitud PUT para actualizar el post existente**
response = requests.put(
    wordpress_url,
    json=post_data,
    auth=(os.getenv("WORDPRESS_USER"), os.getenv("WORDPRESS_PASSWORD"))  # 🔒 Seguridad
)

# **Verificar si la actualización fue exitosa**
if response.status_code == 200:
    print("✅ ¡Publicación de RSI actualizada exitosamente en WordPress!")
else:
    print(f"❌ Error al actualizar RSI: {response.status_code}, {response.text}")

# ESTOCASTICO. Importar librerías necesarias
from tradingview_ta import TA_Handler, Interval
import pandas as pd
import datetime

# Lista de activos y mercados
activos = {
    "SPY": "AMEX", "DJI": "DJI", "NDX": "NASDAQ", "MSFT": "NASDAQ", "GOOGL": "NASDAQ",
    "META": "NASDAQ", "IBM": "NYSE", "V": "NYSE", "JPM": "NYSE", "MA": "NYSE",
    "AAPL": "NASDAQ", "AMD": "NASDAQ", "NVDA": "NASDAQ", "AMZN": "NASDAQ", "KO": "NYSE",
    "NKE": "NYSE", "DIS": "NYSE", "MCD": "NYSE", "NFLX": "NASDAQ", "CAT": "NYSE",
    "TSLA": "NASDAQ", "CVX": "NYSE", "XOM": "NYSE", "JNJ": "NYSE", "BTCUSD": "BINANCE",
    "ETHUSD": "BINANCE"
}

# Temporalidades a analizar
temporalidades_estocastico = {
    "Stoch_4H": Interval.INTERVAL_4_HOURS,
    "Stoch_1D": Interval.INTERVAL_1_DAY,
    "Stoch_1W": Interval.INTERVAL_1_WEEK,
    "Stoch_1M": Interval.INTERVAL_1_MONTH
}

# Recopilar resultados del Estocástico
data_stoch = []

for activo, mercado in activos.items():
    fila_stoch = {"Ticker": activo}
    for nombre_columna, intervalo in temporalidades_estocastico.items():
        try:
            handler = TA_Handler(symbol=activo, exchange=mercado, screener="america", interval=intervalo)
            stoch_k = handler.get_analysis().indicators.get("Stoch.K")
            fila_stoch[nombre_columna] = stoch_k
        except:
            fila_stoch[nombre_columna] = None
    data_stoch.append(fila_stoch)

# Crear DataFrame del Estocástico
df_stoch = pd.DataFrame(data_stoch)

# Convertir a numérico y redondear
for col in temporalidades_estocastico.keys():
    df_stoch[col] = pd.to_numeric(df_stoch[col], errors="coerce").round(2)

# Filtro: Oscilador Estocástico entre 20 y 80
df_stoch_filtrado = df_stoch[
    ((df_stoch[["Stoch_4H", "Stoch_1D", "Stoch_1W", "Stoch_1M"]] <= 20) |
     (df_stoch[["Stoch_4H", "Stoch_1D", "Stoch_1W", "Stoch_1M"]] >= 80)).any(axis=1)
]

# Mostrar resultados
print(f"📈 Estocástico entre 20 y 80 - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
print(df_stoch_filtrado)

import requests
import datetime
import pandas as pd
import os  # Para manejar variables de entorno

# ⚠️ **ID de WordPress para el Estocástico**
post_id_stoch = "998"  # ⚠️ Cambia esto con el ID correcto de WordPress

# URL de la API para actualizar el post
wordpress_url_stoch = f"https://estrategiaelite.com/wp-json/wp/v2/posts/{post_id_stoch}"

# **Función para aplicar colores según valores**
def aplicar_colores(valor):
    if pd.notna(valor):  # Evita errores con valores nulos
        if valor <= 20:
            return f'<span style="color: #009900; font-weight: bold;">{valor}</span>'  # Verde
        elif valor >= 80:
            return f'<span style="color: #FF0000; font-weight: bold;">{valor}</span>'  # Rojo
    return f'<span style="font-weight: bold;">{valor}</span>'  # Negrita sin color

# **Aplicar formato de colores al Estocástico**
df_stoch_coloreado = df_stoch_filtrado.copy()
for col in ["Stoch_4H", "Stoch_1D", "Stoch_1W", "Stoch_1M"]:
    df_stoch_coloreado[col] = df_stoch_coloreado[col].apply(aplicar_colores)

# **Diseño de la tabla en HTML con estilos**
def generar_tabla_html(df):
    estilos = """
    <style>
        table {border-collapse: collapse; width: 100%; font-family: Arial;}
        th, td {border: 1px solid #ddd; padding: 10px; text-align: center;}
        th {background-color: #0073aa; color: white; font-weight: bold;}
        tr:nth-child(even) {background-color: #f2f2f2;}
        tr:hover {background-color: #ddd;}
    </style>
    """
    return estilos + df.to_html(index=False, escape=False)

# **Datos de la actualización**
post_data_stoch = {
    "title": f"Oscilador Estocástico - Actualización {datetime.datetime.now().strftime('%Y-%m-%d')}",
    "content": generar_tabla_html(df_stoch_coloreado)
}

# **Ejecutar la solicitud PUT para actualizar el post en WordPress**
response_stoch = requests.put(
    wordpress_url_stoch,
    json=post_data_stoch,
    auth=(os.getenv("WORDPRESS_USER"), os.getenv("WORDPRESS_PASSWORD"))  # 🔒 Seguridad en GitHub
)

# **Confirmación del éxito**
if response_stoch.status_code == 200:
    print("✅ ¡Publicación del Oscilador Estocástico actualizada exitosamente en WordPress!")
else:
    print(f"❌ Error al actualizar el Estocástico: {response_stoch.status_code}, {response_stoch.text}")

# APERTURAS MENSUALES INDICADOR
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Definir los tickers y sus mercados
tickers_info = {
    "SPY": "AMEX", "^DJI": "DJI", "NDX": "NASDAQ", "MSFT": "NASDAQ", "GOOGL": "NASDAQ",
    "META": "NASDAQ", "IBM": "NYSE", "V": "NYSE", "JPM": "NYSE", "MA": "NYSE",
    "AAPL": "NASDAQ", "AMD": "NASDAQ", "NVDA": "NASDAQ", "AMZN": "NASDAQ", "KO": "NYSE",
    "NKE": "NYSE", "DIS": "NYSE", "MCD": "NYSE", "NFLX": "NASDAQ", "CAT": "NYSE",
    "TSLA": "NASDAQ", "CVX": "NYSE", "XOM": "NYSE", "JNJ": "NYSE"
}

# Convertir a lista de tickers
tickers = list(tickers_info.keys())

# Definir el rango de fechas: últimos 7 meses
end_date = datetime.today()
start_date = end_date - timedelta(days=210)

# Descargar datos de los tickers
data = yf.download(tickers, start=start_date, end=end_date, interval='1d', group_by='ticker', auto_adjust=False)

# Función para obtener la apertura del primer día hábil de cada mes
def get_monthly_openings(df):
    monthly_open = df.resample('MS').first()  # 'MS' = Month Start
    return monthly_open[['Open']]

# Crear una lista para almacenar resultados
resultados = []

# Procesar cada ticker
for ticker in tickers:
    try:
        df = data[ticker].dropna()
        df.index = pd.to_datetime(df.index)

        # Precio actual
        precio_actual = df['Close'].iloc[-1]

        # Aperturas mensuales
        monthly_open = get_monthly_openings(df)
        monthly_open = monthly_open.tail(6)

        # Comparar cada mes
        for fecha, row in monthly_open.iterrows():
            apertura = row['Open']
            diferencia = (precio_actual - apertura) / apertura * 100  # en %

            if -1 <= diferencia <= 1:
                resultados.append({
                    'Ticker': ticker,
                    'Mes': fecha.strftime('%Y-%m'),
                    'Apertura Mensual': round(apertura, 2),
                    'Precio Actual': round(precio_actual, 2),
                    'Diferencia (%)': round(diferencia, 2)
                })
    except Exception as e:
        print(f"Error procesando {ticker}: {e}")

# Mostrar resultados
df_resultados = pd.DataFrame(resultados).sort_values(by=['Mes', 'Ticker'])
print(df_resultados)  # ✅ Reemplazo `display()` por `print()`

import requests
import datetime
import os  # Para manejar variables de entorno

# ⚠️ **ID de WordPress para Aperturas Mensuales**
post_id_aperturas = "990"  # ⚠️ Usa el ID correcto de WordPress

# URL de la API para actualizar el post
wordpress_url_aperturas = f"https://estrategiaelite.com/wp-json/wp/v2/posts/{post_id_aperturas}"

# **Función para aplicar formato al DataFrame**
def aplicar_colores(valor):
    if pd.notna(valor):
        return f'<span style="font-weight: bold;">{valor}</span>'  # Negrita para todos
    return str(valor)

# **Copiar DataFrame y aplicar formato**
df_aperturas_coloreado = df_resultados.copy()
for col in ["Apertura Mensual", "Precio Actual", "Diferencia (%)"]:
    df_aperturas_coloreado[col] = df_aperturas_coloreado[col].apply(aplicar_colores)

# **Diseño de la tabla en HTML**
def generar_tabla_html(df):
    estilos = """
    <style>
        table {border-collapse: collapse; width: 100%; font-family: Arial;}
        th, td {border: 1px solid #ddd; padding: 10px; text-align: center;}
        th {background-color: #0073aa; color: white; font-weight: bold;}
        tr:nth-child(even) {background-color: #f2f2f2;}
        tr:hover {background-color: #ddd;}
    </style>
    """
    return estilos + df.to_html(index=False, escape=False)

# **Datos de la actualización**
post_data_aperturas = {
    "title": f"Aperturas Mensuales de Activos - {datetime.datetime.now().strftime('%Y-%m-%d')}",
    "content": generar_tabla_html(df_aperturas_coloreado)
}

# **Ejecutar la solicitud PUT para actualizar el post en WordPress**
response_aperturas = requests.put(
    wordpress_url_aperturas,
    json=post_data_aperturas,
    auth=(os.getenv("WORDPRESS_USER"), os.getenv("WORDPRESS_PASSWORD"))  # 🔒 Seguridad en GitHub
)

# **Confirmación del éxito**
if response_aperturas.status_code == 200:
    print("✅ ¡Publicación de Aperturas Mensuales actualizada exitosamente en WordPress!")
else:
    print(f"❌ Error al actualizar Aperturas Mensuales: {response_aperturas.status_code}, {response_aperturas.text}")

