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
        row["RSI_1M"] <= 30, row["RSI_1M"] >= 70
    ])

# **Función para verificar condiciones del Estocástico**
def cumple_condicion_stoch(row):
    return any([
        row["Stoch_4H"] <= 20, row["Stoch_4H"] >= 80,
        row["Stoch_1D"] <= 20, row["Stoch_1D"] >= 80,
        row["Stoch_1W"] <= 20, row["Stoch_1W"] >= 80,
        row["Stoch_1M"] <= 20, row["Stoch_1M"] >= 80
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
for col in ["RSI_4H", "RSI_1D", "RSI_1W", "RSI_1M"]:
    df_coloreado[col] = df_coloreado[col].apply(lambda x: aplicar_colores(x, "RSI"))
for col in ["Stoch_4H", "Stoch_1D", "Stoch_1W", "Stoch_1M"]:
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

# MA 200 
from tradingview_ta import TA_Handler, Interval
import pandas as pd

# **Lista de activos con su mercado en TradingView**
assets = {
    "SPY": "AMEX", "DJI": "DJI", "NDX": "NASDAQ", "MSFT": "NASDAQ", "GOOGL": "NASDAQ",
    "META": "NASDAQ", "IBM": "NYSE", "V": "NYSE", "JPM": "NYSE", "MA": "NYSE",
    "AAPL": "NASDAQ", "AMD": "NASDAQ", "NVDA": "NASDAQ", "AMZN": "NASDAQ", "KO": "NYSE",
    "NKE": "NYSE", "DIS": "NYSE", "MCD": "NYSE", "NFLX": "NASDAQ", "CAT": "NYSE",
    "TSLA": "NASDAQ", "CVX": "NYSE", "XOM": "NYSE", "JNJ": "NYSE"
}

# **Intervalos de TradingView**
intervals_ma200 = {
    "Semanal": Interval.INTERVAL_1_WEEK,
    "Mensual": Interval.INTERVAL_1_MONTH
}

# **Diccionario para almacenar los datos**
data_ma_200 = []
filtered_ma_200 = []

# **Obtención de datos desde TradingView**
for asset, market in assets.items():
    asset_data = {"Activo": asset}

    for period_name, interval in intervals_ma200.items():
        try:
            handler = TA_Handler(symbol=asset, exchange=market, screener="america", interval=interval)
            analysis = handler.get_analysis()

            price = analysis.indicators.get("close", None)  # Precio actual
            ma_200 = analysis.indicators.get("SMA200", None)  # Media móvil de 200

            asset_data[f"Precio_{period_name}"] = price
            asset_data[f"200_MA_{period_name}"] = ma_200

            # **Calcular el rango en porcentaje**
            if price and ma_200:
                rango = ((price - ma_200) / ma_200) * 100
                asset_data[f"Rango_{period_name}"] = rango

                # **Filtrar si el rango está dentro de ±1%**
                if -1 <= rango <= 1:
                    filtered_ma_200.append(asset_data)

        except Exception as e:
            print(f"Error obteniendo datos para {asset} ({period_name}): {e}")

    data_ma_200.append(asset_data)

# **Conversión a DataFrame**
df_ma_200 = pd.DataFrame(data_ma_200)
df_filtrado_ma_200 = pd.DataFrame(filtered_ma_200)  # ✅ Renombrado para evitar conflictos

# **Mostrar todos los datos**
print("📊 Datos completos de la MA200:")
print(df_ma_200)

# **Mostrar activos dentro del rango ±1% de la MA200**
print("\n✅ Activos dentro del rango ±1% de la MA200:")
print(df_filtrado_ma_200)

# MA 50 
from tradingview_ta import TA_Handler, Interval
import pandas as pd

# **Lista de activos con su mercado en TradingView**
assets = {
    "SPY": "AMEX", "DJI": "DJI", "NDX": "NASDAQ", "MSFT": "NASDAQ", "GOOGL": "NASDAQ",
    "META": "NASDAQ", "IBM": "NYSE", "V": "NYSE", "JPM": "NYSE", "MA": "NYSE",
    "AAPL": "NASDAQ", "AMD": "NASDAQ", "NVDA": "NASDAQ", "AMZN": "NASDAQ", "KO": "NYSE",
    "NKE": "NYSE", "DIS": "NYSE", "MCD": "NYSE", "NFLX": "NASDAQ", "CAT": "NYSE",
    "TSLA": "NASDAQ", "CVX": "NYSE", "XOM": "NYSE", "JNJ": "NYSE"
}

# **Intervalos de TradingView**
intervals_ma50 = {
    "Semanal": Interval.INTERVAL_1_WEEK,
    "Mensual": Interval.INTERVAL_1_MONTH
}

# **Diccionario para almacenar los datos**
data_ma_50 = []
filtered_ma_50 = []

# **Obtención de datos desde TradingView**
for asset, market in assets.items():
    asset_data = {"Activo": asset}

    for period_name, interval in intervals_ma50.items():
        try:
            handler = TA_Handler(symbol=asset, exchange=market, screener="america", interval=interval)
            analysis = handler.get_analysis()

            price = analysis.indicators.get("close", None)  # Precio actual
            ma_50 = analysis.indicators.get("SMA50", None)  # Media móvil de 50

            asset_data[f"Precio_{period_name}"] = price
            asset_data[f"50_MA_{period_name}"] = ma_50

            # **Calcular el rango en porcentaje**
            if price and ma_50:
                rango = ((price - ma_50) / ma_50) * 100
                asset_data[f"Rango_{period_name}"] = rango

                # **Filtrar si el rango está dentro de ±2%**
                if -2 <= rango <= 2:
                    filtered_ma_50.append(asset_data)

        except Exception as e:
            print(f"Error obteniendo datos para {asset} ({period_name}): {e}")

    data_ma_50.append(asset_data)

# **Conversión a DataFrame**
df_ma_50 = pd.DataFrame(data_ma_50)
df_filtrado_ma_50 = pd.DataFrame(filtered_ma_50)  # ✅ Renombrado para evitar conflictos

# **Mostrar todos los datos**
print("📊 Datos completos de la MA50:")
print(df_ma_50)

# **Mostrar activos dentro del rango ±2% de la MA50**
print("\n✅ Activos dentro del rango ±2% de la MA50:")
print(df_filtrado_ma_50)

# MA 2O
from tradingview_ta import TA_Handler, Interval
import pandas as pd

# **Lista de activos con su mercado en TradingView**
assets = {
    "SPY": "AMEX", "DJI": "DJI", "NDX": "NASDAQ", "MSFT": "NASDAQ", "GOOGL": "NASDAQ",
    "META": "NASDAQ", "IBM": "NYSE", "V": "NYSE", "JPM": "NYSE", "MA": "NYSE",
    "AAPL": "NASDAQ", "AMD": "NASDAQ", "NVDA": "NASDAQ", "AMZN": "NASDAQ", "KO": "NYSE",
    "NKE": "NYSE", "DIS": "NYSE", "MCD": "NYSE", "NFLX": "NASDAQ", "CAT": "NYSE",
    "TSLA": "NASDAQ", "CVX": "NYSE", "XOM": "NYSE", "JNJ": "NYSE"
}

# **Intervalos de TradingView**
intervals_ma20 = {
    "Semanal": Interval.INTERVAL_1_WEEK,
    "Mensual": Interval.INTERVAL_1_MONTH
}

# **Diccionario para almacenar los datos**
data_ma_20 = []
filtered_ma_20 = []

# **Obtención de datos desde TradingView**
for asset, market in assets.items():
    asset_data = {"Activo": asset}

    for period_name, interval in intervals_ma20.items():
        try:
            handler = TA_Handler(symbol=asset, exchange=market, screener="america", interval=interval)
            analysis = handler.get_analysis()

            price = analysis.indicators.get("close", None)  # Precio actual
            ma_20 = analysis.indicators.get("SMA20", None)  # Media móvil de 20

            asset_data[f"Precio_{period_name}"] = price
            asset_data[f"20_MA_{period_name}"] = ma_20

            # **Calcular el rango en porcentaje**
            if price and ma_20:
                rango = ((price - ma_20) / ma_20) * 100
                asset_data[f"Rango_{period_name}"] = rango

                # **Filtrar si el rango está dentro de ±2%**
                if -2 <= rango <= 2:
                    filtered_ma_20.append(asset_data)

        except Exception as e:
            print(f"Error obteniendo datos para {asset} ({period_name}): {e}")

    data_ma_20.append(asset_data)

# **Conversión a DataFrame**
df_ma_20 = pd.DataFrame(data_ma_20)
df_filtrado_ma_20 = pd.DataFrame(filtered_ma_20)  # ✅ Renombrado para evitar conflictos

# **Mostrar todos los datos**
print("📊 Datos completos de la MA20:")
print(df_ma_20)

# **Mostrar activos dentro del rango ±2% de la MA20**
print("\n✅ Activos dentro del rango ±2% de la MA20:")
print(df_filtrado_ma_20)

# Confluencias MA y Osciladores 
import pandas as pd

# **Renombrar "Activo" a "Ticker" en las medias móviles para coincidir con RSI y Estocástico**
df_ma_20.rename(columns={"Activo": "Ticker"}, inplace=True)
df_ma_50.rename(columns={"Activo": "Ticker"}, inplace=True)
df_ma_200.rename(columns={"Activo": "Ticker"}, inplace=True)

# **Filtrar activos con RSI ≤30 o ≥70**
df_rsi_filtrado = df_rsi[
    (df_rsi[["RSI_4H", "RSI_1D", "RSI_1W", "RSI_1M"]] <= 30).any(axis=1) |
    (df_rsi[["RSI_4H", "RSI_1D", "RSI_1W", "RSI_1M"]] >= 70).any(axis=1)
]

# **Filtrar activos con Estocástico ≤20 o ≥80**
df_stoch_filtrado = df_stoch[
    (df_stoch[["Stoch_4H", "Stoch_1D", "Stoch_1W", "Stoch_1M"]] <= 20).any(axis=1) |
    (df_stoch[["Stoch_4H", "Stoch_1D", "Stoch_1W", "Stoch_1M"]] >= 80).any(axis=1)
]

# **Filtrar activos dentro del rango ±2% de cada MA**
df_ma_20_filtrado = df_ma_20[
    ((df_ma_20["Rango_Semanal"].between(-2, 2)) | (df_ma_20["Rango_Mensual"].between(-2, 2)))
]
df_ma_50_filtrado = df_ma_50[
    ((df_ma_50["Rango_Semanal"].between(-2, 2)) | (df_ma_50["Rango_Mensual"].between(-2, 2)))
]
df_ma_200_filtrado = df_ma_200[
    ((df_ma_200["Rango_Semanal"].between(-2, 2)) | (df_ma_200["Rango_Mensual"].between(-2, 2)))
]

# **Generar DataFrames de confluencias con RSI**
df_confluencia_20_rsi = pd.merge(df_ma_20_filtrado, df_rsi_filtrado, on="Ticker", how="inner")
df_confluencia_50_rsi = pd.merge(df_ma_50_filtrado, df_rsi_filtrado, on="Ticker", how="inner")
df_confluencia_200_rsi = pd.merge(df_ma_200_filtrado, df_rsi_filtrado, on="Ticker", how="inner")

# **Generar DataFrames de confluencias con Estocástico**
df_confluencia_20_stoch = pd.merge(df_ma_20_filtrado, df_stoch_filtrado, on="Ticker", how="inner")
df_confluencia_50_stoch = pd.merge(df_ma_50_filtrado, df_stoch_filtrado, on="Ticker", how="inner")
df_confluencia_200_stoch = pd.merge(df_ma_200_filtrado, df_stoch_filtrado, on="Ticker", how="inner")

# **Mostrar resultados organizados por cada media móvil**
print("\n📊 Activos con confluencia MA 20 ±2% + RSI:")
print(df_confluencia_20_rsi)

print("\n📊 Activos con confluencia MA 50 ±2% + RSI:")
print(df_confluencia_50_rsi)

print("\n📊 Activos con confluencia MA 200 ±2% + RSI:")
print(df_confluencia_200_rsi)

print("\n📊 Activos con confluencia MA 20 ±2% + Estocástico:")
print(df_confluencia_20_stoch)

print("\n📊 Activos con confluencia MA 50 ±2% + Estocástico:")
print(df_confluencia_50_stoch)

print("\n📊 Activos con confluencia MA 200 ±2% + Estocástico:")
print(df_confluencia_200_stoch)

# BANDAS DE BOLLINGER
from tradingview_ta import TA_Handler, Interval
import pandas as pd

# **Lista de activos con su mercado en TradingView**
assets = {
    "SPY": "AMEX", "DJI": "DJI", "NDX": "NASDAQ", "MSFT": "NASDAQ", "GOOGL": "NASDAQ",
    "META": "NASDAQ", "IBM": "NYSE", "V": "NYSE", "JPM": "NYSE", "MA": "NYSE",
    "AAPL": "NASDAQ", "AMD": "NASDAQ", "NVDA": "NASDAQ", "AMZN": "NASDAQ", "KO": "NYSE",
    "NKE": "NYSE", "DIS": "NYSE", "MCD": "NYSE", "NFLX": "NASDAQ", "CAT": "NYSE",
    "TSLA": "NASDAQ", "CVX": "NYSE", "XOM": "NYSE", "JNJ": "NYSE"
}

# **Intervalos de TradingView**
intervals_bb = {
    "Diario": Interval.INTERVAL_1_DAY,
    "Semanal": Interval.INTERVAL_1_WEEK,
    "Mensual": Interval.INTERVAL_1_MONTH
}

# **Diccionario para almacenar los datos**
data_bb = []
filtered_bb = []

# **Obtención de datos desde TradingView**
for asset, market in assets.items():
    asset_data = {"Activo": asset}

    for period_name, interval in intervals_bb.items():
        try:
            handler = TA_Handler(symbol=asset, exchange=market, screener="america", interval=interval)
            analysis = handler.get_analysis()

            price = analysis.indicators.get("close", None)  # Precio actual
            bb_upper = analysis.indicators.get("BB.upper", None)  # Banda Bollinger superior
            bb_lower = analysis.indicators.get("BB.lower", None)  # Banda Bollinger inferior

            asset_data[f"Precio_{period_name}"] = price
            asset_data[f"BB_Upper_{period_name}"] = bb_upper
            asset_data[f"BB_Lower_{period_name}"] = bb_lower

            # **Filtrar activos que cumplan la condición**
            if price and bb_upper and bb_lower:
                if price >= bb_upper or price <= bb_lower:
                    filtered_bb.append(asset_data)

        except Exception as e:
            print(f"Error obteniendo datos para {asset} ({period_name}): {e}")

    data_bb.append(asset_data)

# **Conversión a DataFrame**
df_bb = pd.DataFrame(data_bb)
df_filtrado_bb = pd.DataFrame(filtered_bb)  # ✅ Renombrado para evitar conflictos

# **Mostrar todos los datos**
print("📊 Datos completos de Bandas de Bollinger:")
print(df_bb)

# **Mostrar activos fuera de las bandas de Bollinger**
print("\n✅ Activos fuera de las bandas de Bollinger:")
print(df_filtrado_bb)

 # POST BANDAS DE BOLLINGER
import requests
import datetime
import pandas as pd
import os  # Para manejar variables de entorno

# **ID de WordPress para actualización de Bandas de Bollinger**
post_id_bb = "1020"  # ⚠️ Usa el ID correcto de WordPress

# **URL de la API para actualizar el post**
wordpress_url_bb = f"https://estrategiaelite.com/wp-json/wp/v2/posts/{post_id_bb}"

# **Filtrar los activos fuera de las bandas de Bollinger**
df_filtrado_bb = df_bb[
    (df_bb["Precio_Diario"] >= df_bb["BB_Upper_Diario"]) |
    (df_bb["Precio_Diario"] <= df_bb["BB_Lower_Diario"]) |
    (df_bb["Precio_Semanal"] >= df_bb["BB_Upper_Semanal"]) |
    (df_bb["Precio_Semanal"] <= df_bb["BB_Lower_Semanal"]) |
    (df_bb["Precio_Mensual"] >= df_bb["BB_Upper_Mensual"]) |
    (df_bb["Precio_Mensual"] <= df_bb["BB_Lower_Mensual"])
]

# **Eliminar columnas innecesarias**
df_coloreado_bb = df_filtrado_bb.drop(columns=["Precio_Semanal", "Precio_Mensual"]).copy()

# **Función para aplicar colores**
def aplicar_colores(valor, tipo, umbral):
    if pd.notna(valor):
        if tipo == "superior" and valor >= umbral:
            return f'<span style="color: #FF0000; font-weight: bold;">{valor}</span>'  # Rojo
        elif tipo == "inferior" and valor <= umbral:
            return f'<span style="color: #009900; font-weight: bold;">{valor}</span>'  # Verde
    return str(valor)

# **Aplicar colores al DataFrame**
for col in ["BB_Upper_Diario", "BB_Upper_Semanal", "BB_Upper_Mensual"]:
    df_coloreado_bb[col] = df_coloreado_bb.apply(lambda x: aplicar_colores(x["Precio_Diario"], "superior", x[col]), axis=1)
for col in ["BB_Lower_Diario", "BB_Lower_Semanal", "BB_Lower_Mensual"]:
    df_coloreado_bb[col] = df_coloreado_bb.apply(lambda x: aplicar_colores(x["Precio_Diario"], "inferior", x[col]), axis=1)

# **Modificar nombres de columnas con saltos de línea**
columnas_modificadas_bb = {
    "Precio_Diario": "Precio<br>Diario",
    "BB_Upper_Diario": "Banda<br>Superior<br>Diaria",
    "BB_Lower_Diario": "Banda<br>Inferior<br>Diaria",
    "BB_Upper_Semanal": "Banda<br>Superior<br>Semanal",
    "BB_Lower_Semanal": "Banda<br>Inferior<br>Semanal",
    "BB_Upper_Mensual": "Banda<br>Superior<br>Mensual",
    "BB_Lower_Mensual": "Banda<br>Inferior<br>Mensual",
}

df_coloreado_bb.rename(columns=columnas_modificadas_bb, inplace=True)

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
        return "<p style='text-align:center; font-size:16px; font-weight:bold;'>No hay activos fuera de las bandas de Bollinger</p>"
    return estilos + df.to_html(index=False, escape=False)

# **Datos de la actualización**
post_data_bb = {
    "title": f"Activos fuera de las Bandas de Bollinger - Actualización {datetime.datetime.now().strftime('%Y-%m-%d')}",
    "content": generar_tabla_html(df_coloreado_bb)
}

# **Ejecutar la solicitud PUT para actualizar el post en WordPress**
response_bb = requests.put(
    wordpress_url_bb,
    json=post_data_bb,
    auth=(os.getenv("WORDPRESS_USER"), os.getenv("WORDPRESS_PASSWORD"))  # 🔒 Seguridad en GitHub
)

# **Confirmación del éxito**
if response_bb.status_code == 200:
    print("✅ ¡Publicación de activos fuera de Bollinger actualizada exitosamente en WordPress!")
else:
    print(f"❌ Error al actualizar en WordPress: {response_bb.status_code}, {response_bb.text}")

# confluencias bandas de bollinger Y OSCILADORES
import pandas as pd

# **Renombrar "Activo" a "Ticker" en las Bandas de Bollinger**
df_bb.rename(columns={"Activo": "Ticker"}, inplace=True)

# **Verificar que las columnas necesarias existen antes de fusionar**
columnas_necesarias = ["Precio_Diario", "BB_Upper_Diario", "BB_Lower_Diario", "RSI_1D", "Stoch_1D"]

# **Fusionar DataFrames asegurando que las claves coincidan**
df_combinado = df_bb.merge(df_rsi, on="Ticker", how="inner").merge(df_stoch, on="Ticker", how="inner")

# **Confirmar que todas las columnas necesarias están en df_combinado**
columnas_faltantes = [col for col in columnas_necesarias if col not in df_combinado.columns]

if columnas_faltantes:
    print(f"⚠️ Faltan estas columnas en el DataFrame fusionado: {columnas_faltantes}")
else:
    # **Aplicar filtros de confluencia**
    df_filtrado_confluencias = df_combinado[
        (
            (df_combinado["Precio_Diario"] >= df_combinado["BB_Upper_Diario"]) & 
            ((df_combinado["RSI_1D"] >= 70) | (df_combinado["Stoch_1D"] >= 80))
        ) |
        (
            (df_combinado["Precio_Diario"] <= df_combinado["BB_Lower_Diario"]) & 
            ((df_combinado["RSI_1D"] <= 30) | (df_combinado["Stoch_1D"] <= 20))
        )
    ].copy()

    # **Modificar nombres de columnas para formato HTML**
    columnas_modificadas_confluencias = {
        "Ticker": "Activo",
        "Precio_Diario": "Precio<br>Diario",
        "BB_Upper_Diario": "Banda<br>Superior<br>Diaria",
        "BB_Lower_Diario": "Banda<br>Inferior<br>Diaria",
        "RSI_1D": "RSI<br>Diario",
        "Stoch_1D": "Estocástico<br>Diario",
    }

    df_filtrado_confluencias.rename(columns=columnas_modificadas_confluencias, inplace=True)

    # **Aplicar colores a RSI y Estocástico**
    def aplicar_colores(valor, tipo):
        if pd.notna(valor):
            if tipo == "RSI" and valor >= 70:
                return f'<span style="color: #FF0000; font-weight: bold;">{valor}</span>'  # Rojo
            elif tipo == "RSI" and valor <= 30:
                return f'<span style="color: #009900; font-weight: bold;">{valor}</span>'  # Verde
            elif tipo == "Stoch" and valor >= 80:
                return f'<span style="color: #FF0000; font-weight: bold;">{valor}</span>'  # Rojo
            elif tipo == "Stoch" and valor <= 20:
                return f'<span style="color: #009900; font-weight: bold;">{valor}</span>'  # Verde
        return str(valor)

    for col in ["RSI<br>Diario"]:
        df_filtrado_confluencias[col] = df_filtrado_confluencias[col].apply(lambda x: aplicar_colores(x, "RSI"))
    for col in ["Estocástico<br>Diario"]:
        df_filtrado_confluencias[col] = df_filtrado_confluencias[col].apply(lambda x: aplicar_colores(x, "Stoch"))

    # **Mostrar el DataFrame**
    print("✅ Activos con confluencias entre Bandas de Bollinger, RSI y Estocástico:")
    print(df_filtrado_confluencias)
# Actualizar POst Bandas de BB y osciladores 
import pandas as pd

# **Renombrar "Activo" a "Ticker" en las Bandas de Bollinger**
df_bb.rename(columns={"Activo": "Ticker"}, inplace=True)

# **Verificar que las columnas necesarias existen antes de fusionar**
columnas_necesarias = ["Precio_Diario", "BB_Upper_Diario", "BB_Lower_Diario", "RSI_1D", "Stoch_1D"]

# **Fusionar DataFrames asegurando que las claves coincidan**
df_combinado = df_bb.merge(df_rsi, on="Ticker", how="inner").merge(df_stoch, on="Ticker", how="inner")

# **Confirmar que todas las columnas necesarias están en df_combinado**
columnas_faltantes = [col for col in columnas_necesarias if col not in df_combinado.columns]

if columnas_faltantes:
    print(f"⚠️ Faltan estas columnas en el DataFrame fusionado: {columnas_faltantes}")
else:
    # **Aplicar filtros de confluencia**
    df_filtrado_confluencias = df_combinado[
        (
            (df_combinado["Precio_Diario"] >= df_combinado["BB_Upper_Diario"]) & 
            ((df_combinado["RSI_1D"] >= 70) | (df_combinado["Stoch_1D"] >= 80))
        ) |
        (
            (df_combinado["Precio_Diario"] <= df_combinado["BB_Lower_Diario"]) & 
            ((df_combinado["RSI_1D"] <= 30) | (df_combinado["Stoch_1D"] <= 20))
        )
    ].copy()

    # **Modificar nombres de columnas para formato HTML**
    columnas_modificadas_confluencias = {
        "Ticker": "Activo",
        "Precio_Diario": "Precio<br>Diario",
        "BB_Upper_Diario": "Banda<br>Superior<br>Diaria",
        "BB_Lower_Diario": "Banda<br>Inferior<br>Diaria",
        "RSI_1D": "RSI<br>Diario",
        "Stoch_1D": "Estocástico<br>Diario",
    }

    df_filtrado_confluencias.rename(columns=columnas_modificadas_confluencias, inplace=True)

    # **Aplicar colores a RSI y Estocástico**
    def aplicar_colores(valor, tipo):
        if pd.notna(valor):
            if tipo == "RSI" and valor >= 70:
                return f'<span style="color: #FF0000; font-weight: bold;">{valor}</span>'  # Rojo
            elif tipo == "RSI" and valor <= 30:
                return f'<span style="color: #009900; font-weight: bold;">{valor}</span>'  # Verde
            elif tipo == "Stoch" and valor >= 80:
                return f'<span style="color: #FF0000; font-weight: bold;">{valor}</span>'  # Rojo
            elif tipo == "Stoch" and valor <= 20:
                return f'<span style="color: #009900; font-weight: bold;">{valor}</span>'  # Verde
        return str(valor)

    for col in ["RSI<br>Diario"]:
        df_filtrado_confluencias[col] = df_filtrado_confluencias[col].apply(lambda x: aplicar_colores(x, "RSI"))
    for col in ["Estocástico<br>Diario"]:
        df_filtrado_confluencias[col] = df_filtrado_confluencias[col].apply(lambda x: aplicar_colores(x, "Stoch"))

    # **Mostrar el DataFrame**
    print("✅ Activos con confluencias entre Bandas de Bollinger, RSI y Estocástico:")
    print(df_filtrado_confluencias)
# Publicacion confluencias BB y estoc
import requests
import datetime
import pandas as pd
import os  # Para manejar variables de entorno

# **ID de WordPress para actualización de confluencias**
post_id_confluencias = "1028"  # ⚠️ Usa el ID correcto de WordPress

# **URL de la API para actualizar el post**
wordpress_url_confluencias = f"https://estrategiaelite.com/wp-json/wp/v2/posts/{post_id_confluencias}"

# **Eliminar columnas innecesarias solo si existen**
columnas_a_eliminar = ["Precio_Semanal", "Precio_Mensual"]
df_coloreado_confluencias = df_filtrado_confluencias.drop(
    columns=[col for col in columnas_a_eliminar if col in df_filtrado_confluencias.columns]
).copy()

# **Redondear precios y Bandas de Bollinger a 2 decimales**
columnas_a_redondear = [
    "Precio<br>Diario", "Banda<br>Superior<br>Diaria", "Banda<br>Inferior<br>Diaria",
    "BB_Upper_Semanal", "BB_Lower_Semanal", "BB_Upper_Mensual", "BB_Lower_Mensual"
]
for col in columnas_a_redondear:
    if col in df_coloreado_confluencias.columns:
        df_coloreado_confluencias[col] = df_coloreado_confluencias[col].astype(float).round(2)

# **Modificar nombres de columnas para formato HTML**
columnas_modificadas_confluencias = {
    "Precio<br>Diario": "Precio<br>D",
    "Banda<br>Superior<br>Diaria": "BB Up<br>D",
    "Banda<br>Inferior<br>Diaria": "BB Low<br>D",
    "BB_Upper_Semanal": "BB Up<br>W",
    "BB_Lower_Semanal": "BB Low<br>W",
    "BB_Upper_Mensual": "BB Up<br>M",
    "BB_Lower_Mensual": "BB Low<br>M",
    "RSI_1D": "RSI<br>D",
    "RSI_1W": "RSI<br>W",
    "RSI_1M": "RSI<br>M",
    "Stoch_1D": "Stoch<br>D",
    "Stoch_1W": "Stoch<br>W",
    "Stoch_1M": "Stoch<br>M",
}

df_coloreado_confluencias.rename(columns=columnas_modificadas_confluencias, inplace=True)

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
        return "<p style='text-align:center; font-size:16px; font-weight:bold;'>No hay confluencias</p>"
    return estilos + df.to_html(index=False, escape=False)

# **Datos de la actualización**
post_data_confluencias = {
    "title": f"Confluencias entre BB, RSI y Stoch - Actualización {datetime.datetime.now().strftime('%Y-%m-%d')}",
    "content": generar_tabla_html(df_coloreado_confluencias)
}

# **Ejecutar la solicitud PUT para actualizar el post en WordPress**
response_confluencias = requests.put(
    wordpress_url_confluencias,
    json=post_data_confluencias,
    auth=(os.getenv("WORDPRESS_USER"), os.getenv("WORDPRESS_PASSWORD"))  # 🔒 Seguridad en GitHub
)

# **Confirmación del éxito**
if response_confluencias.status_code == 200:
    print("✅ ¡Publicación de confluencias actualizada exitosamente en WordPress!")
else:
    print(f"❌ Error al actualizar en WordPress: {response_confluencias.status_code}, {response_confluencias.text}")





