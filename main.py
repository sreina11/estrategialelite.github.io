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
}

# Temporalidades
temporalidades = {
    "RSI_4H": Interval.INTERVAL_4_HOURS,
    "RSI_1D": Interval.INTERVAL_1_DAY,
    "RSI_1W": Interval.INTERVAL_1_WEEK,
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
    (df_rsi[["RSI_4H", "RSI_1D", "RSI_1W"]] <= 30).any(axis=1) |
    (df_rsi[["RSI_4H", "RSI_1D", "RSI_1W"]] >= 70).any(axis=1)
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
for col in ["RSI_4H", "RSI_1D", "RSI_1W"]:
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
    "TSLA": "NASDAQ", "CVX": "NYSE", "XOM": "NYSE", "JNJ": "NYSE"
}

# Temporalidades a analizar
temporalidades_estocastico = {
    "Stoch_4H": Interval.INTERVAL_4_HOURS,
    "Stoch_1D": Interval.INTERVAL_1_DAY,
    "Stoch_1W": Interval.INTERVAL_1_WEEK,
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
    ((df_stoch[["Stoch_4H", "Stoch_1D", "Stoch_1W"]] <= 20) |
     (df_stoch[["Stoch_4H", "Stoch_1D", "Stoch_1W"]] >= 80)).any(axis=1)
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
for col in ["Stoch_4H", "Stoch_1D", "Stoch_1W"]:
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

# CONFLUENCIAS APERTURAS Y OSCILADORES RSI Y STOC
import pandas as pd

# **Eliminar duplicados en df_resultados antes de unir**
df_resultados_unicos = df_resultados.drop_duplicates(subset=["Ticker"])

# **Merge con RSI y Estocástico**
df_combinado = df_resultados_unicos.merge(df_rsi, on="Ticker", how="inner").merge(df_stoch, on="Ticker", how="inner")

# **Función para verificar condiciones del RSI**
def cumple_condicion_rsi(row):
    return any([
        row["RSI_4H"] <= 30, row["RSI_4H"] >= 70,
        row["RSI_1D"] <= 30, row["RSI_1D"] >= 70,
        row["RSI_1W"] <= 30, row["RSI_1W"] >= 70,
    ])

# **Función para verificar condiciones del Estocástico**
def cumple_condicion_stoch(row):
    return any([
        row["Stoch_4H"] <= 20, row["Stoch_4H"] >= 80,
        row["Stoch_1D"] <= 20, row["Stoch_1D"] >= 80,
        row["Stoch_1W"] <= 20, row["Stoch_1W"] >= 80,
    ])

# **Aplicar filtros**
df_filtrado_final = df_combinado[df_combinado.apply(
    lambda row: cumple_condicion_rsi(row) or cumple_condicion_stoch(row), axis=1
)]

# **Mostrar resultado final**
print("✅ Activos cerca de la apertura mensual ±1% y con RSI o Estocástico extremos:")
print(df_filtrado_final.sort_values(by="Ticker"))  # ✅ Reemplazo `display()` por `print()`

# POST CONFLUENCIAS APERTURAS RSI STOCH
import requests
import datetime
import pandas as pd
import os  # Para manejar variables de entorno

# ⚠️ **ID de WordPress para Confluencias Técnicas**
post_id_confluencias = "1032"  # ⚠️ Usa el ID correcto de WordPress

# URL de la API para actualizar el post
wordpress_url_confluencias = f"https://estrategiaelite.com/wp-json/wp/v2/posts/{post_id_confluencias}"

# **Función para aplicar formato de colores**
def aplicar_colores(valor, tipo):
    if pd.notna(valor):
        if tipo == "RSI":
            if valor >= 70:
                return f'<span style="color: red; font-weight: bold;">{valor}</span>'  # Sobrecompra
            elif valor <= 30:
                return f'<span style="color: green; font-weight: bold;">{valor}</span>'  # Sobreventa
        elif tipo == "Stoch":
            if valor >= 80:
                return f'<span style="color: red; font-weight: bold;">{valor}</span>'  # Sobrecompra
            elif valor <= 20:
                return f'<span style="color: green; font-weight: bold;">{valor}</span>'  # Sobreventa
    return f'<span style="font-weight: bold;">{valor}</span>'  # Negrita sin color

# **Aplicar colores al DataFrame**
df_coloreado = df_filtrado_final.copy()
for col in ["RSI_4H", "RSI_1D", "RSI_1W"]:
    df_coloreado[col] = df_coloreado[col].apply(lambda x: aplicar_colores(x, "RSI"))
for col in ["Stoch_4H", "Stoch_1D", "Stoch_1W"]:
    df_coloreado[col] = df_coloreado[col].apply(lambda x: aplicar_colores(x, "Stoch"))

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
post_data_confluencias = {
    "title": f"Confluencias Técnicas - {datetime.datetime.now().strftime('%Y-%m-%d')}",
    "content": generar_tabla_html(df_coloreado)
}

# **Ejecutar la solicitud PUT para actualizar el post en WordPress**
response_confluencias = requests.put(
    wordpress_url_confluencias,
    json=post_data_confluencias,
    auth=(os.getenv("WORDPRESS_USER"), os.getenv("WORDPRESS_PASSWORD"))  # 🔒 Seguridad en GitHub
)

# **Confirmación del éxito**
if response_confluencias.status_code == 200:
    print("✅ ¡Publicación de Confluencias Técnicas actualizada exitosamente en WordPress!")
else:
    print(f"❌ Error al actualizar Confluencias: {response_confluencias.status_code}, {response_confluencias.text}")

# Medias moviles Precio y rango

import yfinance as yf
import pandas as pd
import requests
import os
import datetime
import time

tickers = [
    "AAPL", "AMD", "AMZN", "CAT", "CVX", "DIS", "GOOGL", "IBM", "JNJ", "JPM",
    "KO", "MA", "MCD", "META", "MSFT", "^NDX", "NFLX", "NKE", "NVDA", "SPY",
    "TSLA", "V", "XOM", "^DJI"
]

def pct_diff(price, ma):
    """Calcula la diferencia porcentual respecto a la media móvil."""
    return round(((price - ma) / ma) * 100, 2) if price and ma else None

def get_ma_data(ticker, interval, label):
    """Obtiene las medias móviles y el precio actual de un ticker."""
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period="max", interval=interval, auto_adjust=True)

        if hist.empty:
            print(f"⚠️ No se encontraron datos para {ticker} ({label})")
            return pd.Series({'Ticker': ticker, 'Precio Actual': None})

        close = hist['Close'].iloc[-1]
        ma20 = hist['Close'].rolling(window=20).mean().iloc[-1] if len(hist) >= 20 else None
        ma50 = hist['Close'].rolling(window=50).mean().iloc[-1] if len(hist) >= 50 else None
        ma200 = hist['Close'].rolling(window=200).mean().iloc[-1] if len(hist) >= 200 else None

        return pd.Series({
            'Ticker': ticker,
            'Precio Actual': round(close, 2),
            f'{label}_MA20': round(ma20, 2) if ma20 else None,
            f'{label}_MA50': round(ma50, 2) if ma50 else None,
            f'{label}_MA200': round(ma200, 2) if ma200 else None,
            f'{label}_%vsMA20': pct_diff(close, ma20),
            f'{label}_%vsMA50': pct_diff(close, ma50),
            f'{label}_%vsMA200': pct_diff(close, ma200),
        })

    except Exception as e:
        print(f"❌ Error al obtener datos de {ticker}: {e}")
        return pd.Series({'Ticker': ticker, 'Precio Actual': None})


# Obtener dataframes
df_daily = pd.DataFrame([get_ma_data(ticker, "1d", "D") for ticker in tickers])
time.sleep(5)
df_weekly = pd.DataFrame([get_ma_data(ticker, "1wk", "W") for ticker in tickers])
time.sleep(5)
df_monthly = pd.DataFrame([get_ma_data(ticker, "1mo", "M") for ticker in tickers])

# Sumar % de diferencia y ordenar por fortaleza relativa
df_daily['D_Suma%'] = df_daily[['D_%vsMA20', 'D_%vsMA50', 'D_%vsMA200']].apply(
    lambda row: sum([x for x in row if pd.notnull(x)]), axis=1)
df_weekly['W_Suma%'] = df_weekly[['W_%vsMA20', 'W_%vsMA50', 'W_%vsMA200']].apply(
    lambda row: sum([x for x in row if pd.notnull(x)]), axis=1)
df_monthly['M_Suma%'] = df_monthly[['M_%vsMA20', 'M_%vsMA50', 'M_%vsMA200']].apply(
    lambda row: sum([x for x in row if pd.notnull(x)]), axis=1)

df_daily = df_daily.sort_values(by='D_Suma%', ascending=False)
df_weekly = df_weekly.sort_values(by='W_Suma%', ascending=False)
df_monthly = df_monthly.sort_values(by='M_Suma%', ascending=False)

# Función HTML
def to_html_table(df, title):
    return f"<h2>{title}</h2>" + df.to_html(index=False, border=0, classes="wp-block-table", justify='center')

# Crear HTML con tablas ordenadas
html_content = (
    f"<p>Última actualización: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}</p>"
    + "<h2>📊 Activos ordenados por fortaleza técnica</h2>"
    + to_html_table(df_daily, "Media Móvil Diaria")
    + to_html_table(df_weekly, "Media Móvil Semanal")
    + to_html_table(df_monthly, "Media Móvil Mensual")
)

# Publicar en WordPress
post_id = "3016"
url = f"https://estrategiaelite.com/wp-json/wp/v2/posts/{post_id}"

payload = {
    "title": f"Resumen Técnico - {datetime.datetime.now().strftime('%Y-%m-%d')}",
    "content": html_content
}

response = requests.put(
    url,
    json=payload,
    auth=(os.getenv("WORDPRESS_USER"), os.getenv("WORDPRESS_PASSWORD"))
)

if response.status_code == 200:
    print("✅ Publicación actualizada correctamente.")
else:
    print(f"❌ Error al actualizar: {response.status_code} - {response.text}")



# Confluencias Medias moviles + Osciladores
import requests
import pandas as pd
from bs4 import BeautifulSoup
import os

# --- URLs de las páginas ---
url_rsi = 'https://estrategiaelite.com/indice-rsi-publicacion-inicial-2025-05-11/'
url_stoch = 'https://estrategiaelite.com/oscilador-estocastico-2025-05-11/'
url_ma = 'https://estrategiaelite.com/medias-mobiles-acciones-indices/'

# --- Función para extraer tablas de una página ---
def get_tables_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return pd.read_html(str(soup))

# --- Descargar y asignar las tablas ---
rsi_tables = get_tables_from_url(url_rsi)
stoch_tables = get_tables_from_url(url_stoch)
ma_tables = get_tables_from_url(url_ma)

# Asumiendo que el orden es correcto:
df_rsi = rsi_tables[0]
df_stoch = stoch_tables[0]

df_ma_daily = ma_tables[0]
df_ma_weekly = ma_tables[1]
df_ma_monthly = ma_tables[2]

# --- Función para verificar si rango está dentro de ±1% ---
def is_near_ma(rango):
    return abs(rango) <= 1.0

# --- Inicializar listas de resultados ---
rsi_resultados = []
stoch_resultados = []

# --- Unificar tickers ---
tickers = set(df_rsi['Ticker']) | set(df_stoch['Ticker']) | set(df_ma_daily['Ticker'])

# --- Procesar cada ticker ---
for ticker in tickers:
    rsi_row = df_rsi[df_rsi['Ticker'] == ticker]
    stoch_row = df_stoch[df_stoch['Ticker'] == ticker]
    row_daily = df_ma_daily[df_ma_daily['Ticker'] == ticker]
    row_weekly = df_ma_weekly[df_ma_weekly['Ticker'] == ticker]
    row_monthly = df_ma_monthly[df_ma_monthly['Ticker'] == ticker]

    # Recolectar info de precios y rangos
    rangos_ma = []

    def add_ma(source_row, prefix):
        if not source_row.empty:
            for ma in ['20', '50', '200']:
                col_pct = f'{prefix}_%vsMA{ma}'
                col_ma = f'{prefix}_MA{ma}'
                if col_pct in source_row.columns and col_ma in source_row.columns:
                    try:
                        rango = float(source_row[col_pct].values[0])
                        precio_ma = float(source_row[col_ma].values[0])
                        if is_near_ma(rango):
                            rangos_ma.append({
                                'Media Móvil': f'{prefix}_MA{ma}',
                                'Precio Media Móvil': precio_ma,
                                'Rango (%)': round(rango, 2)
                            })
                    except:
                        continue

    add_ma(row_daily, 'D')
    add_ma(row_weekly, 'W')
    add_ma(row_monthly, 'M')

    if not rangos_ma:
        continue

    # Obtener precio actual
    precio_actual = None
    for df in [row_daily, row_weekly, row_monthly]:
        if not df.empty and 'Precio Actual' in df.columns:
            precio_actual = float(df['Precio Actual'].values[0])
            break

    # RSI
    if not rsi_row.empty:
        for col in rsi_row.columns:
            if 'RSI_' in col:
                try:
                    valor = float(rsi_row[col].values[0])
                    if valor <= 30 or valor >= 70:
                        for match in rangos_ma:
                            rsi_resultados.append({
                                'Ticker': ticker,
                                'Precio Actual': precio_actual,
                                'Media Móvil': match['Media Móvil'],
                                'Precio Media Móvil': match['Precio Media Móvil'],
                                'Rango (%)': match['Rango (%)'],
                                'RSI (temporalidad)': col.replace("RSI_", ""),
                                'Valor': valor
                            })
                except:
                    continue

    # Estocástico
    if not stoch_row.empty:
        for col in stoch_row.columns:
            if 'Stoch_' in col:
                try:
                    valor = float(stoch_row[col].values[0])
                    if valor <= 20 or valor >= 80:
                        for match in rangos_ma:
                            stoch_resultados.append({
                                'Ticker': ticker,
                                'Precio Actual': precio_actual,
                                'Media Móvil': match['Media Móvil'],
                                'Precio Media Móvil': match['Precio Media Móvil'],
                                'Rango (%)': match['Rango (%)'],
                                'Stoch (temporalidad)': col.replace("Stoch_", ""),
                                'Valor': valor
                            })
                except:
                    continue

# --- Crear dataframes finales ---
df_rsi_final = pd.DataFrame(rsi_resultados)
df_stoch_final = pd.DataFrame(stoch_resultados)

# --- Convertir los dataframes a HTML ---
html_rsi = "<h4> Confluencias RSI + MA</h4>" + df_rsi_final.to_html(index=False, escape=False)
html_stoch = "<h4> Confluencias Stoch + MA</h4>" + df_stoch_final.to_html(index=False, escape=False)
html_tabla = html_rsi + "<br><br>" + html_stoch

# --- Datos para la actualización del post ---
wordpress_url = "https://estrategiaelite.com/wp-json/wp/v2/posts/1015"
titulo = "🔄 Actualización Confluencias: Osciladores + Medias Móviles"

post_data = {
    "title": titulo,
    "content": html_tabla
}

# --- Enviar actualización ---
response = requests.put(
    wordpress_url,
    json=post_data,
    auth=(os.getenv("WORDPRESS_USER"), os.getenv("WORDPRESS_PASSWORD"))
)

# --- Resultado ---
if response.status_code == 200:
    print("✅ ¡Post actualizado con éxito!")
else:
    print(f"❌ Error al actualizar post: {response.status_code}, {response.text}")

# BANDAS DE BOLLINGER

import requests
from tradingview_ta import TA_Handler, Interval
import pandas as pd
import datetime
import os

# ----------- Configuración de activos y temporalidades -----------
assets = {
    "NDX": "NASDAQ", "MSFT": "NASDAQ", "GOOGL": "NASDAQ",
    "META": "NASDAQ", "IBM": "NYSE", "V": "NYSE", "JPM": "NYSE", "MA": "NYSE",
    "AAPL": "NASDAQ", "AMD": "NASDAQ", "NVDA": "NASDAQ", "AMZN": "NASDAQ", "KO": "NYSE",
    "NKE": "NYSE", "DIS": "NYSE", "MCD": "NYSE", "NFLX": "NASDAQ", "CAT": "NYSE",
    "TSLA": "NASDAQ", "CVX": "NYSE", "XOM": "NYSE", "JNJ": "NYSE"
}

temporalidades = {
    "Diario": Interval.INTERVAL_1_DAY,
    "Semanal": Interval.INTERVAL_1_WEEK,
    "Mensual": Interval.INTERVAL_1_MONTH
}

# ----------- Función de análisis por activo y temporalidad -----------

def analizar_ticker(ticker, exchange):
    datos_rsi = {}
    datos_stoch = {}
    precios = {}

    for nombre, intervalo in temporalidades.items():
        try:
            handler = TA_Handler(symbol=ticker, exchange=exchange, screener="america", interval=intervalo)
            analysis = handler.get_analysis()
            precios[nombre] = {
                "Precio actual": round(analysis.indicators["close"], 2),
                "BB_UP": round(analysis.indicators["BB.upper"], 2),
                "BB_Low": round(analysis.indicators["BB.lower"], 2)
            }
            datos_rsi[nombre] = round(analysis.indicators["RSI"], 2)
            datos_stoch[nombre] = round(analysis.indicators["Stoch.K"], 2)
        except Exception as e:
            print(f"Error en {ticker} - {nombre}: {e}")
            precios[nombre] = {"Precio actual": None, "BB_UP": None, "BB_Low": None}
            datos_rsi[nombre] = None
            datos_stoch[nombre] = None

    try:
        handler_4h = TA_Handler(symbol=ticker, exchange=exchange, screener="america", interval=Interval.INTERVAL_4_HOURS)
        analysis_4h = handler_4h.get_analysis()
        datos_rsi["4H"] = round(analysis_4h.indicators["RSI"], 2)
        datos_stoch["4H"] = round(analysis_4h.indicators["Stoch.K"], 2)
    except:
        datos_rsi["4H"] = None
        datos_stoch["4H"] = None

    return precios, datos_rsi, datos_stoch

# ----------- Recolectar datos por indicador -----------

bb_rsi = {"Diario": [], "Semanal": [], "Mensual": []}
bb_stoch = {"Diario": [], "Semanal": [], "Mensual": []}

for ticker, exchange in assets.items():
    precios, rsi, stoch = analizar_ticker(ticker, exchange)

    for timeframe in temporalidades.keys():
        # Confluencias BB + RSI
        p = precios[timeframe]
        if (p["Precio actual"] >= p["BB_UP"] or p["Precio actual"] <= p["BB_Low"]) and (
            rsi["4H"] >= 70 or rsi["4H"] <= 30 or rsi[timeframe] >= 70 or rsi[timeframe] <= 30
        ):
            bb_rsi[timeframe].append({
                "Ticker": ticker,
                "Precio actual": p["Precio actual"],
                "Precio BB_UP": p["BB_UP"],
                "Precio BB_Low": p["BB_Low"],
                "RSI_4H": rsi["4H"],
                "RSI Diario": rsi.get("Diario"),
                "RSI Semanal": rsi.get("Semanal"),
                "RSI Mensual": rsi.get("Mensual")
            })

        # Confluencias BB + Estocástico
        if (p["Precio actual"] >= p["BB_UP"] or p["Precio actual"] <= p["BB_Low"]) and (
            stoch["4H"] >= 80 or stoch["4H"] <= 20 or stoch[timeframe] >= 80 or stoch[timeframe] <= 20
        ):
            bb_stoch[timeframe].append({
                "Ticker": ticker,
                "Precio actual": p["Precio actual"],
                "Precio BB_UP": p["BB_UP"],
                "Precio BB_Low": p["BB_Low"],
                "STOCH_4H": stoch["4H"],
                "STOCH Diario": stoch.get("Diario"),
                "STOCH Semanal": stoch.get("Semanal"),
            })

# ----------- Funciones para dar formato HTML -----------

def colorear(valor, tipo):
    if pd.isna(valor): return ""
    valor = round(valor, 2)
    if tipo == "RSI":
        if valor >= 70:
            return f'<span style="color:red; font-weight:bold;">{valor}</span>'
        elif valor <= 30:
            return f'<span style="color:green; font-weight:bold;">{valor}</span>'
    elif tipo == "STOCH":
        if valor >= 80:
            return f'<span style="color:red; font-weight:bold;">{valor}</span>'
        elif valor <= 20:
            return f'<span style="color:green; font-weight:bold;">{valor}</span>'
    return str(valor)

def generar_tabla(datos, columnas, tipo="RSI"):
    if not datos:
        return "<p>No hay confluencias.</p>"

    df = pd.DataFrame(datos)
    for col in df.columns:
        if "RSI" in col:
            df[col] = df[col].apply(lambda x: colorear(x, "RSI"))
        elif "STOCH" in col:
            df[col] = df[col].apply(lambda x: colorear(x, "STOCH"))

    estilos = """
    <style>
        table {border-collapse: collapse; width: 100%; font-family: Arial; font-size: 14px;}
        th {border: 1px solid #ccc; padding: 6px; background-color: #004080; color: white;}
        td {border: 1px solid #ccc; padding: 6px; text-align: center;}
        tr:nth-child(even) {background-color: #f2f2f2;}
    </style>
    """
    return estilos + df.to_html(index=False, columns=columnas, escape=False)

# ----------- Crear contenido HTML -----------

contenido = "<h4>Bandas de bollinger Y RSI</h4><br>"
for tf in ["Diario", "Semanal", "Mensual"]:
    contenido += f"<h5 style='margin-left:20px;'>{tf}</h5>"
    columnas = ["Ticker", "Precio actual", "Precio BB_UP", "Precio BB_Low",
                "RSI_4H", "RSI Diario", "RSI Semanal", "RSI Mensual"]
    contenido += generar_tabla(bb_rsi[tf], columnas, "RSI")

contenido += "<h4>Bandas de bollinger y Estocastico</h4><br>"
for tf in ["Diario", "Semanal", "Mensual"]:
    contenido += f"<h5 style='margin-left:20px;'>{tf}</h5>"
    columnas = ["Ticker", "Precio actual", "Precio BB_UP", "Precio BB_Low",
                "STOCH_4H", "STOCH Diario", "STOCH Semanal", "STOCH Mensual"]
    contenido += generar_tabla(bb_stoch[tf], columnas, "STOCH")

# ----------- Publicar en WordPress -----------

post_id = "1028"
url = f"https://estrategiaelite.com/wp-json/wp/v2/posts/{post_id}"

payload = {
    "title": f"Confluencias de Osciladores y Bandas de Bollinger - {datetime.datetime.now().strftime('%Y-%m-%d')}",
    "content": contenido
}

response = requests.put(
    url,
    json=payload,
    auth=(os.getenv("WORDPRESS_USER"), os.getenv("WORDPRESS_PASSWORD"))
)

if response.status_code == 200:
    print("✅ Publicación actualizada correctamente.")
else:
    print(f"❌ Error al actualizar: {response.status_code} - {response.text}")

# INDICADORES ECONOMICOS

import requests
from bs4 import BeautifulSoup
import pandas as pd

# **Lista de indicadores económicos y sus URLs**
indicadores = {
    "Tasa de Interés": "https://www.myfxbook.com/forex-economic-calendar/united-states/fed-interest-rate-decision",
    "PMI (Purchasing Manager Index)": "https://www.myfxbook.com/forex-economic-calendar/united-states/sp-global-manufacturing-pmi",
    "CPI (Índice de Precios al Consumidor)": "https://www.myfxbook.com/forex-economic-calendar/united-states/inflation-rate-yoy",
    "PPI (Producer Price Index)": "https://www.myfxbook.com/forex-economic-calendar/united-states/ppi-yoy",
    "Consumer Confidence": "https://www.myfxbook.com/forex-economic-calendar/united-states/cb-consumer-confidence",
    "Jobless Claims": "https://www.myfxbook.com/forex-economic-calendar/united-states/initial-jobless-claims",
    "Non-Farm Payroll": "https://www.myfxbook.com/forex-economic-calendar/united-states/non-farm-payrolls",
    "GDP (Producto Interno Bruto)": "https://www.myfxbook.com/forex-economic-calendar/united-states/gdp-growth-rate-qoq",
    "Retail Sales": "https://www.myfxbook.com/forex-economic-calendar/united-states/retail-sales-mom",
    "Trade Balance": "https://www.myfxbook.com/forex-economic-calendar/united-states/goods-trade-balance"
}

# **Selectores CSS**
selectores_css = {
    "Fecha": 'div:nth-child(3) > div > div:nth-child(3) > div:nth-child(2) > span:nth-child(2)',
    "Actual": 'div:nth-child(3) > div > div:nth-child(2) > div:nth-child(4) > span:nth-child(2) > span',
    "Anterior": 'div:nth-child(3) > div > div:nth-child(2) > div:nth-child(2) > span:nth-child(2) > span',
    "Esperado": 'div:nth-child(3) > div > div:nth-child(2) > div:nth-child(3) > span:nth-child(2)'
}

# **Lista para almacenar los datos**
datos = []

# **Extraer datos de cada indicador**
headers = {"User-Agent": "Mozilla/5.0"}
for indicador, url in indicadores.items():
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Verifica si la respuesta es válida (código 200)

        soup = BeautifulSoup(response.text, "html.parser")

        # **Extraer cada dato usando selectores CSS**
        datos_evento = {
            "Indicador": indicador,
            "Fecha": soup.select_one(selectores_css["Fecha"]).text.strip() if soup.select_one(selectores_css["Fecha"]) else "No disponible",
            "Actual": soup.select_one(selectores_css["Actual"]).text.strip() if soup.select_one(selectores_css["Actual"]) else "No disponible",
            "Anterior": soup.select_one(selectores_css["Anterior"]).text.strip() if soup.select_one(selectores_css["Anterior"]) else "No disponible",
            "Esperado": soup.select_one(selectores_css["Esperado"]).text.strip() if soup.select_one(selectores_css["Esperado"]) else "No disponible"
        }

        datos.append(datos_evento)

    except requests.exceptions.RequestException as e:
        print(f"❌ Error al obtener datos para {indicador}: {e}")

# **Convertir a DataFrame**
df_indicadores_economicos = pd.DataFrame(datos)

# **Mostrar el DataFrame**
print("📊 Indicadores Económicos obtenidos de MyFXBook:")
print(df_indicadores_economicos)

# POST INDICADORES ECONOMICOS

import requests
import datetime
import pandas as pd
import os  # Para manejar variables de entorno

# **ID de WordPress para actualización de indicadores económicos**
post_id_economia = "1045"  # ⚠️ Usa el ID correcto de WordPress

# **URL de la API para actualizar el post**
wordpress_url_economia = f"https://estrategiaelite.com/wp-json/wp/v2/posts/{post_id_economia}"

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
    if df.empty:
        return "<p style='text-align:center; font-size:16px; font-weight:bold;'>No hay datos disponibles</p>"
    return estilos + df.to_html(index=False, escape=False)

# **Usamos el DataFrame generado previamente**
post_data_economia = {
    "title": f"Indicadores Económicos - Actualización {datetime.datetime.now().strftime('%Y-%m-%d')}",
    "content": generar_tabla_html(df_indicadores_economicos)  # ✅ Usamos el DataFrame correcto
}

# **Ejecutar la solicitud PUT para actualizar el post en WordPress**
response_economia = requests.put(
    wordpress_url_economia,
    json=post_data_economia,
    auth=(os.getenv("WORDPRESS_USER"), os.getenv("WORDPRESS_PASSWORD"))  # 🔒 Seguridad en GitHub
)

# **Confirmación del éxito**
if response_economia.status_code == 200:
    print("✅ ¡Publicación de indicadores económicos actualizada exitosamente en WordPress!")
else:
    print(f"❌ Error al actualizar en WordPress: {response_economia.status_code}, {response_economia.text}")


#---------------------------------------------------------------------------------------------
# ANALISIS MACRO
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import os

# **Configuración de WordPress**
POST_ID = "1125"
WORDPRESS_URL = f"https://estrategiaelite.com/wp-json/wp/v2/posts/{POST_ID}"
WP_USER = os.getenv("WORDPRESS_USER")
WP_PASSWORD = os.getenv("WORDPRESS_PASSWORD")

# **Lista de indicadores económicos y sus URLs**
indicadores = {
    "Tasa de Interés": "https://www.myfxbook.com/forex-economic-calendar/united-states/fed-interest-rate-decision",
    "PMI": "https://www.myfxbook.com/forex-economic-calendar/united-states/sp-global-manufacturing-pmi",
    "CPI": "https://www.myfxbook.com/forex-economic-calendar/united-states/inflation-rate-yoy",
    "PPI": "https://www.myfxbook.com/forex-economic-calendar/united-states/ppi-yoy",
    "Consumer Confidence": "https://www.myfxbook.com/forex-economic-calendar/united-states/cb-consumer-confidence",
    "Jobless Claims": "https://www.myfxbook.com/forex-economic-calendar/united-states/initial-jobless-claims",
    "Non-Farm Payroll": "https://www.myfxbook.com/forex-economic-calendar/united-states/non-farm-payrolls",
    "GDP": "https://www.myfxbook.com/forex-economic-calendar/united-states/gdp-growth-rate-qoq",
    "Retail Sales": "https://www.myfxbook.com/forex-economic-calendar/united-states/retail-sales-mom",
    "Trade Balance": "https://www.myfxbook.com/forex-economic-calendar/united-states/goods-trade-balance"
}

# **Impacto por clase de activo**
impacto_matriz = {
    "Tasa de Interés": {"Forex": 3, "Acciones": -3, "Bonos": -3, "Commodities": -2, "Criptomonedas": -3},
    "PMI": {"Forex": 2, "Acciones": 3, "Bonos": 2, "Commodities": 1, "Criptomonedas": 2},
    "CPI": {"Forex": 3, "Acciones": -3, "Bonos": -3, "Commodities": -3, "Criptomonedas": -3},
    "PPI": {"Forex": 2, "Acciones": 2, "Bonos": -3, "Commodities": 2, "Criptomonedas": 2},
    "Consumer Confidence": {"Forex": 1, "Acciones": 2, "Bonos": 1, "Commodities": 0, "Criptomonedas": 2},
    "Jobless Claims": {"Forex": -2, "Acciones": 2, "Bonos": -2, "Commodities": 0, "Criptomonedas": 2},
    "Non-Farm Payroll": {"Forex": 3, "Acciones": -3, "Bonos": -3, "Commodities": 2, "Criptomonedas": -3},
    "GDP": {"Forex": 2, "Acciones": 3, "Bonos": 2, "Commodities": 1, "Criptomonedas": 3},
    "Retail Sales": {"Forex": 2, "Acciones": 3, "Bonos": 2, "Commodities": 1, "Criptomonedas": 2},
    "Trade Balance": {"Forex": 3, "Acciones": 1, "Bonos": 0, "Commodities": 2, "Criptomonedas": 1}
}

# **Selectores CSS**
selectores_css = {
    "Fecha": 'div:nth-child(3) > div > div:nth-child(3) > div:nth-child(2) > span:nth-child(2)',
    "Actual": 'div:nth-child(3) > div > div:nth-child(2) > div:nth-child(4) > span:nth-child(2) > span',
    "Esperado": 'div:nth-child(3) > div > div:nth-child(2) > div:nth-child(3) > span:nth-child(2)'
}

# **Extraer datos de cada indicador**
datos = []
headers = {"User-Agent": "Mozilla/5.0"}
for indicador, url in indicadores.items():
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        actual_raw = soup.select_one(selectores_css["Actual"])
        esperado_raw = soup.select_one(selectores_css["Esperado"])

        actual = actual_raw.text.strip().replace('%', '').replace('K', '').replace('$', '').replace(',', '') if actual_raw else "No disponible"
        esperado = esperado_raw.text.strip().replace('%', '').replace('K', '').replace('$', '').replace(',', '') if esperado_raw else "No disponible"

        datos_evento = {
            "Indicador": indicador,
            "Fecha": soup.select_one(selectores_css["Fecha"]).text.strip() if soup.select_one(selectores_css["Fecha"]) else "No disponible",
            "Actual": float(actual) if actual.replace('.', '', 1).isdigit() else "No disponible",
            "Esperado": float(esperado) if esperado.replace('.', '', 1).isdigit() else "No disponible"
        }

        datos_evento["Impacto"] = (
            1 if datos_evento["Actual"] > datos_evento["Esperado"] else
            -1 if datos_evento["Actual"] < datos_evento["Esperado"] else 0
        ) if datos_evento["Actual"] != "No disponible" and datos_evento["Esperado"] != "No disponible" else 0

        datos.append(datos_evento)

    except Exception as e:
        print(f"❌ Error obteniendo datos para {indicador}: {e}")

# **Convertir a DataFrame**
df_indicadores_economicos = pd.DataFrame(datos)

# **Calcular impacto final por activo**
impacto_final = {activo: sum(df_indicadores_economicos.apply(lambda x: x["Impacto"] * impacto_matriz[x["Indicador"]][activo], axis=1)) for activo in impacto_matriz["Tasa de Interés"]}

# **Clasificación del impacto**
def clasificar_impacto(valor):
    if valor >= 4:
        return "Positivo Alto"
    elif 1 <= valor <= 3:
        return "Positivo Medio"
    elif valor == 0:
        return "Neutral"
    elif -1 >= valor >= -3:
        return "Negativo Medio"
    else:
        return "Negativo Alto"

impacto_clasificado = {activo: clasificar_impacto(valor) for activo, valor in impacto_final.items()}

# **Publicar en WordPress**
post_data = {"content": f"<div id='impacto_economico'><h4>Impacto Económico ({datetime.datetime.now().strftime('%Y-%m-%d')})</h4><ul>{''.join([f'<li><strong>{activo}:</strong> {impacto_clasificado[activo]}</li>' for activo in impacto_clasificado])}</ul></div>"}
response = requests.put(WORDPRESS_URL, json=post_data, auth=(WP_USER, WP_PASSWORD))

if response.status_code == 200:
    print("✅ ¡Post actualizado correctamente en WordPress!")
else:
    print(f"❌ Error al actualizar el post: {response.status_code}, {response.text}")


