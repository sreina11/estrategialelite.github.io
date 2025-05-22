# RSI. Activos y mercado
from tradingview_ta import TA_Handler, Interval
import pandas as pd
import datetime

activos = {
    "BTCUSDT": "BINANCE",
    "ETHUSDT": "BINANCE",
    "XRPUSDT": "BINANCE",
    "BNBUSDT": "BINANCE",
    "SOLUSDT": "BINANCE",
    "DOGEUSDT": "BINANCE",
    "ADAUSDT": "BINANCE",
    "AVAXUSDT": "BINANCE",
    "XLMUSDT": "BINANCE",
    "HYPEUSDT": "BINANCE",
    "SHIBUSDT": "BINANCE",
    "LINKUSDT": "BINANCE",
    "SUIUSDT": "BINANCE",
    "WAXPUSDT": "BINANCE",
    "PAXGUSDT": "BINANCE"
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
                screener="crypto",
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
post_id = "1326"  # ⚠️ Usa el ID correcto generado antes

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
    "BTCUSDT": "BINANCE",
    "ETHUSDT": "BINANCE",
    "XRPUSDT": "BINANCE",
    "BNBUSDT": "BINANCE",
    "SOLUSDT": "BINANCE",
    "DOGEUSDT": "BINANCE",
    "ADAUSDT": "BINANCE",
    "AVAXUSDT": "BINANCE",
    "XLMUSDT": "BINANCE",
    "HYPEUSDT": "BINANCE",
    "SHIBUSDT": "BINANCE",
    "LINKUSDT": "BINANCE",
    "SUIUSDT": "BINANCE",
    "WAXPUSDT": "BINANCE",
    "PAXGUSDT": "BINANCE"
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
            handler = TA_Handler(symbol=activo, exchange=mercado, screener="crypto", interval=intervalo)
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
post_id_stoch = "1334"  # ⚠️ Cambia esto con el ID correcto de WordPress

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

# Medias moviles 

# MA 200 
from tradingview_ta import TA_Handler, Interval
import pandas as pd

# **Lista de activos con su mercado en TradingView**
assets = {
    "BTCUSDT": "BINANCE",
    "ETHUSDT": "BINANCE",
    "XRPUSDT": "BINANCE",
    "BNBUSDT": "BINANCE",
    "SOLUSDT": "BINANCE",
    "DOGEUSDT": "BINANCE",
    "ADAUSDT": "BINANCE",
    "AVAXUSDT": "BINANCE",
    "XLMUSDT": "BINANCE",
    "SHIBUSDT": "BINANCE",
    "LINKUSDT": "BINANCE",
    "SUIUSDT": "BINANCE",
    "WAXPUSDT": "BINANCE",
    "PAXGUSDT": "BINANCE"
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
            handler = TA_Handler(symbol=asset, exchange=market, screener="crypto", interval=interval)
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
    "BTCUSDT": "BINANCE",
    "ETHUSDT": "BINANCE",
    "XRPUSDT": "BINANCE",
    "BNBUSDT": "BINANCE",
    "SOLUSDT": "BINANCE",
    "DOGEUSDT": "BINANCE",
    "ADAUSDT": "BINANCE",
    "AVAXUSDT": "BINANCE",
    "XLMUSDT": "BINANCE",
    "SHIBUSDT": "BINANCE",
    "LINKUSDT": "BINANCE",
    "SUIUSDT": "BINANCE",
    "WAXPUSDT": "BINANCE",
    "PAXGUSDT": "BINANCE"
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
            handler = TA_Handler(symbol=asset, exchange=market, screener="crypto", interval=interval)
            analysis = handler.get_analysis()

            price = analysis.indicators.get("close", None)  # Precio actual
            ma_50 = analysis.indicators.get("SMA50", None)  # Media móvil de 50

            asset_data[f"Precio_{period_name}"] = price
            asset_data[f"50_MA_{period_name}"] = ma_50

            # **Calcular el rango en porcentaje**
            if price and ma_50:
                rango = ((price - ma_50) / ma_50) * 100
                asset_data[f"Rango_{period_name}"] = rango

                # **Filtrar si el rango está dentro de ±1%**
                if -1 <= rango <= 1:
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

# **Mostrar activos dentro del rango ±1% de la MA50**
print("\n✅ Activos dentro del rango ±1% de la MA50:")
print(df_filtrado_ma_50)

# MA 2O
from tradingview_ta import TA_Handler, Interval
import pandas as pd

# **Lista de activos con su mercado en TradingView**
assets = {
    "BTCUSDT": "BINANCE",
    "ETHUSDT": "BINANCE",
    "XRPUSDT": "BINANCE",
    "BNBUSDT": "BINANCE",
    "SOLUSDT": "BINANCE",
    "DOGEUSDT": "BINANCE",
    "ADAUSDT": "BINANCE",
    "AVAXUSDT": "BINANCE",
    "XLMUSDT": "BINANCE",
    "SHIBUSDT": "BINANCE",
    "LINKUSDT": "BINANCE",
    "SUIUSDT": "BINANCE",
    "WAXPUSDT": "BINANCE",
    "PAXGUSDT": "BINANCE"
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
            handler = TA_Handler(symbol=asset, exchange=market, screener="crypto", interval=interval)
            analysis = handler.get_analysis()

            price = analysis.indicators.get("close", None)  # Precio actual
            ma_20 = analysis.indicators.get("SMA20", None)  # Media móvil de 20

            asset_data[f"Precio_{period_name}"] = price
            asset_data[f"20_MA_{period_name}"] = ma_20

            # **Calcular el rango en porcentaje**
            if price and ma_20:
                rango = ((price - ma_20) / ma_20) * 100
                asset_data[f"Rango_{period_name}"] = rango

                # **Filtrar si el rango está dentro de ±1%**
                if -1 <= rango <= 1:
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

# **Mostrar activos dentro del rango ±1% de la MA20**
print("\n✅ Activos dentro del rango ±1% de la MA20:")
print(df_filtrado_ma_20)

# CONFLUENCIAS MEDIAS MOVILES Y RSI

from tradingview_ta import TA_Handler, Interval
import pandas as pd
import datetime
import requests
import os  # Para autenticación en WordPress

# Activos y mercado
activos = {
    "BTCUSDT": "BINANCE", "ETHUSDT": "BINANCE", "XRPUSDT": "BINANCE", "BNBUSDT": "BINANCE",
    "SOLUSDT": "BINANCE", "DOGEUSDT": "BINANCE", "ADAUSDT": "BINANCE", "AVAXUSDT": "BINANCE",
    "XLMUSDT": "BINANCE", "SHIBUSDT": "BINANCE", "LINKUSDT": "BINANCE", "SUIUSDT": "BINANCE",
    "WAXPUSDT": "BINANCE", "PAXGUSDT": "BINANCE"
}

# Intervalos de medias móviles
intervalos_ma = {
    "Semanal": Interval.INTERVAL_1_WEEK,
    "Mensual": Interval.INTERVAL_1_MONTH
}

# Diccionario para almacenar los datos filtrados
data_filtrada = []

# Obtención de datos desde TradingView
for activo, mercado in activos.items():
    datos_activo = {"Ticker": activo}
    cumple_confluencia = False  # Bandera para detectar si el activo cumple con la condición

    for periodo, intervalo in intervalos_ma.items():
        try:
            handler = TA_Handler(symbol=activo, exchange=mercado, screener="crypto", interval=intervalo)
            analysis = handler.get_analysis()

            precio = analysis.indicators.get("close", None)  # Precio actual
            ma = analysis.indicators.get("SMA200", None)  # Media móvil de 200

            datos_activo[f"Precio_{periodo}"] = round(precio, 2) if precio else None
            datos_activo[f"MA200_{periodo}"] = round(ma, 2) if ma else None

            # Calcular rango en porcentaje
            if precio and ma:
                rango = ((precio - ma) / ma) * 100
                datos_activo[f"Rango_{periodo}"] = round(rango, 2)

                # Verificar si está dentro de ±1%
                if -1 <= rango <= 1:
                    cumple_confluencia = True

        except Exception as e:
            print(f"Error obteniendo datos para {activo} ({periodo}): {e}")

    # Si el activo cumple con la confluencia, se añade a la lista
    if cumple_confluencia:
        data_filtrada.append(datos_activo)

# Generar tabla HTML
def generar_tabla_html(df):
    estilos = """
    <style>
        table {border-collapse: collapse; width: 100%; font-family: Arial;}
        th {background-color: #0073aa; color: white; font-weight: bold; padding: 8px; border: 1px solid #ddd;}
        td {padding: 8px; border: 1px solid #ddd; text-align: center;}
        tr:nth-child(even) {background-color: #f9f9f9;}
    </style>
    """
    return estilos + df.to_html(index=False, escape=False)

df_filtrado = pd.DataFrame(data_filtrada)
html_tabla = generar_tabla_html(df_filtrado) if not df_filtrado.empty else "<p>No hay activos en el rango de ±1%</p>"

# Publicar en WordPress
post_id = "1339"
wordpress_url = f"https://estrategiaelite.com/wp-json/wp/v2/posts/{post_id}"
titulo = f"Activos en el rango de MA200 ({datetime.datetime.now().strftime('%Y-%m-%d')})"

post_data = {
    "title": titulo,
    "content": html_tabla
}

response = requests.put(
    wordpress_url,
    json=post_data,
    auth=(os.getenv("WORDPRESS_USER"), os.getenv("WORDPRESS_PASSWORD"))
)

if response.status_code == 200:
    print("Post actualizado con éxito")
else:
    print(f"Error al actualizar post: {response.status_code}, {response.text}")

# BANDAS DE BOLLINGER Y OSCILADORES

import requests
from tradingview_ta import TA_Handler, Interval
import pandas as pd
import datetime
import os
import re  # Importamos el módulo para limpiar HTML

# ----------- Configuración de activos y temporalidades -----------
activos = {
    "BTCUSDT": "BINANCE", "ETHUSDT": "BINANCE", "XRPUSDT": "BINANCE",
    "BNBUSDT": "BINANCE", "SOLUSDT": "BINANCE", "DOGEUSDT": "BINANCE",
    "ADAUSDT": "BINANCE", "AVAXUSDT": "BINANCE", "XLMUSDT": "BINANCE",
    "SHIBUSDT": "BINANCE", "LINKUSDT": "BINANCE", "SUIUSDT": "BINANCE",
    "WAXPUSDT": "BINANCE", "PAXGUSDT": "BINANCE"
}

temporalidades = {
    "Diario": Interval.INTERVAL_1_DAY,
    "Semanal": Interval.INTERVAL_1_WEEK,
    "Mensual": Interval.INTERVAL_1_MONTH
}

# ----------- Función de análisis por activo y temporalidad -----------
def analizar_ticker(ticker, exchange):
    precios = {}
    datos_rsi = {}
    datos_stoch = {}

    for nombre, intervalo in temporalidades.items():
        try:
            handler = TA_Handler(symbol=ticker, exchange=exchange, screener="crypto", interval=intervalo)
            analysis = handler.get_analysis()
            precio_actual = round(analysis.indicators["close"], 4)  # 4 decimales
            bb_up = round(analysis.indicators["BB.upper"], 2)
            bb_low = round(analysis.indicators["BB.lower"], 2)

            precios[nombre] = {
                "Precio actual": precio_actual,
                "BB_UP": bb_up,
                "BB_Low": bb_low
            }

            rsi = round(analysis.indicators["RSI"], 2)
            datos_rsi[nombre] = f'<span style="color:{"red" if rsi >= 70 else "green" if rsi <= 20 else "black"}">{rsi}</span>'

            stoch = round(analysis.indicators["Stoch.K"], 2)
            datos_stoch[nombre] = f'<span style="color:{"red" if stoch >= 80 else "green" if stoch <= 20 else "black"}">{stoch}</span>'

        except Exception as e:
            print(f"Error en {ticker} - {nombre}: {e}")
            precios[nombre] = {"Precio actual": None, "BB_UP": None, "BB_Low": None}
            datos_rsi[nombre] = None
            datos_stoch[nombre] = None

    return precios, datos_rsi, datos_stoch

# ----------- Recolectar datos en tiempo real -----------
bb_rsi = {"Diario": [], "Semanal": [], "Mensual": []}
bb_stoch = {"Diario": [], "Semanal": [], "Mensual": []}

for ticker, exchange in activos.items():
    precios, rsi, stoch = analizar_ticker(ticker, exchange)

    for timeframe in temporalidades.keys():
        p = precios[timeframe]

        if p["Precio actual"] is not None:
            bb_up_num = p["BB_UP"]
            bb_low_num = p["BB_Low"]

            # Negrilla en precio de BB más cercano
            if abs(p["Precio actual"] - bb_up_num) < abs(p["Precio actual"] - bb_low_num):
                p["BB_UP"] = f"<b>{bb_up_num}</b>"
            else:
                p["BB_Low"] = f"<b>{bb_low_num}</b>"

            # Convertir RSI a número antes de comparar
            rsi_numerico = float(re.sub(r'<[^>]+>', '', rsi[timeframe]))

            # Convertir Estocástico a número antes de comparar
            stoch_numerico = float(re.sub(r'<[^>]+>', '', stoch[timeframe]))

            # Confluencias BB + RSI
            if (p["Precio actual"] >= bb_up_num or p["Precio actual"] <= bb_low_num) and (
                rsi_numerico >= 70 or rsi_numerico <= 20
            ):
                bb_rsi[timeframe].append({
                    "Ticker": ticker,
                    "Precio actual": p["Precio actual"],
                    "Precio BB_UP": p["BB_UP"],
                    "Precio BB_Low": p["BB_Low"],
                    "RSI Diario": rsi.get("Diario"),
                    "RSI Semanal": rsi.get("Semanal"),
                    "RSI Mensual": rsi.get("Mensual")
                })

            # Confluencias BB + Estocástico
            if (p["Precio actual"] >= bb_up_num or p["Precio actual"] <= bb_low_num) and (
                stoch_numerico >= 80 or stoch_numerico <= 20
            ):
                bb_stoch[timeframe].append({
                    "Ticker": ticker,
                    "Precio actual": p["Precio actual"],
                    "Precio BB_UP": p["BB_UP"],
                    "Precio BB_Low": p["BB_Low"],
                    "STOCH Diario": stoch.get("Diario"),
                    "STOCH Semanal": stoch.get("Semanal"),
                    "STOCH Mensual": stoch.get("Mensual")
                })

# ----------- Publicar en WordPress -----------
post_id = "1380"
url = f"https://estrategiaelite.com/wp-json/wp/v2/posts/{post_id}"

payload = {
    "title": f"Confluencias de Osciladores y Bandas de Bollinger – {datetime.datetime.now().strftime('%Y-%m-%d')}",
    "content": f"<h4>Confluencias de Osciladores y Bandas de Bollinger</h4>"
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

import requests
from tradingview_ta import TA_Handler, Interval
import pandas as pd
import datetime
import os

# ----------- Configuración de activos y temporalidades -----------
activos = {
    "BTCUSDT": "BINANCE", "ETHUSDT": "BINANCE", "XRPUSDT": "BINANCE",
    "BNBUSDT": "BINANCE", "SOLUSDT": "BINANCE", "DOGEUSDT": "BINANCE",
    "ADAUSDT": "BINANCE", "AVAXUSDT": "BINANCE", "XLMUSDT": "BINANCE",
    "SHIBUSDT": "BINANCE", "LINKUSDT": "BINANCE", "SUIUSDT": "BINANCE",
    "WAXPUSDT": "BINANCE", "PAXGUSDT": "BINANCE"
}

temporalidades = {
    "Diario": Interval.INTERVAL_1_DAY,
    "Semanal": Interval.INTERVAL_1_WEEK,
    "Mensual": Interval.INTERVAL_1_MONTH
}

# ----------- Función de análisis por activo y temporalidad -----------
def analizar_ticker(ticker, exchange):
    precios = {}
    datos_rsi = {}
    datos_stoch = {}

    for nombre, intervalo in temporalidades.items():
        try:
            handler = TA_Handler(symbol=ticker, exchange=exchange, screener="crypto", interval=intervalo)
            analysis = handler.get_analysis()
            precios[nombre] = {
                "Precio actual": round(analysis.indicators["close"], 5),
                "BB_UP": round(analysis.indicators["BB.upper"], 5),
                "BB_Low": round(analysis.indicators["BB.lower"], 5)
            }
            datos_rsi[nombre] = round(analysis.indicators["RSI"], 2)
            datos_stoch[nombre] = round(analysis.indicators["Stoch.K"], 2)
        except Exception as e:
            print(f"Error en {ticker} - {nombre}: {e}")
            precios[nombre] = {"Precio actual": None, "BB_UP": None, "BB_Low": None}
            datos_rsi[nombre] = None
            datos_stoch[nombre] = None

    try:
        handler_4h = TA_Handler(symbol=ticker, exchange=exchange, screener="crypto", interval=Interval.INTERVAL_4_HOURS)
        analysis_4h = handler_4h.get_analysis()
        datos_rsi["4H"] = round(analysis_4h.indicators["RSI"], 2)
        datos_stoch["4H"] = round(analysis_4h.indicators["Stoch.K"], 2)
    except:
        datos_rsi["4H"] = None
        datos_stoch["4H"] = None

    return precios, datos_rsi, datos_stoch

# ----------- Recolectar datos en tiempo real -----------
bb_rsi = {"Diario": [], "Semanal": [], "Mensual": []}
bb_stoch = {"Diario": [], "Semanal": [], "Mensual": []}

for ticker, exchange in activos.items():
    precios, rsi, stoch = analizar_ticker(ticker, exchange)

    for timeframe in temporalidades.keys():
        p = precios[timeframe]

        if p["Precio actual"] is not None:
            # Confluencias BB + RSI
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
                    "STOCH Mensual": stoch.get("Mensual")
                })

# ----------- Generar contenido HTML -----------
def generar_tabla(datos, columnas):
    if not datos:
        return "<p>No hay confluencias.</p>"
    
    df = pd.DataFrame(datos)

    # Redondear valores específicos a 5 decimales
    for col in ["Precio actual", "Precio BB_UP", "Precio BB_Low"]:
        if col in df.columns:
            df[col] = df[col].astype(float).round(5)

    estilos = """
    <style>
        table {border-collapse: collapse; width: 100%; font-family: Arial; font-size: 14px;}
        th {border: 1px solid #ccc; padding: 6px; background-color: #004080; color: white;}
        td {border: 1px solid #ccc; padding: 6px; text-align: center;}
        tr:nth-child(even) {background-color: #f2f2f2;}
    </style>
    """
    
    return estilos + df.to_html(index=False, columns=columnas, escape=False)

# Definir fecha actual
fecha_actual = datetime.datetime.now().strftime('%Y-%m-%d')

contenido = f"<h4>Confluencias de Osciladores y Bandas de Bollinger – {fecha_actual}</h4><br>"

contenido += "<h4>Bandas de Bollinger y RSI</h4><br>"
for tf in ["Diario", "Semanal", "Mensual"]:
    contenido += f"<h5>{tf}</h5>"
    columnas_rsi = ["Ticker", "Precio actual", "Precio BB_UP", "Precio BB_Low", "RSI_4H", "RSI Diario", "RSI Semanal", "RSI Mensual"]
    contenido += generar_tabla(bb_rsi[tf], columnas_rsi)

contenido += "<h4>Bandas de Bollinger y Estocástico</h4><br>"
for tf in ["Diario", "Semanal", "Mensual"]:
    contenido += f"<h5>{tf}</h5>"
    columnas_stoch = ["Ticker", "Precio actual", "Precio BB_UP", "Precio BB_Low", "STOCH_4H", "STOCH Diario", "STOCH Semanal", "STOCH Mensual"]
    contenido += generar_tabla(bb_stoch[tf], columnas_stoch)

# ----------- Publicar en WordPress -----------
post_id = "1380"
url = f"https://estrategiaelite.com/wp-json/wp/v2/posts/{post_id}"

payload = {
    "title": f"Confluencias de Osciladores y Bandas de Bollinger – {fecha_actual}",
    "content": contenido
}

response = requests.put(url, json=payload, auth=(os.getenv("WORDPRESS_USER"), os.getenv("WORDPRESS_PASSWORD")))

print("✅ Publicación actualizada correctamente." if response.status_code == 200 else f"❌ Error al actualizar: {response.status_code} - {response.text}")

# APERTURAS
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import requests
import os  # Para manejar variables de entorno
from requests.auth import HTTPBasicAuth

# **Lista de criptomonedas**
symbols = {
    "BTCUSDT": "BTC-USD", "ETHUSDT": "ETH-USD", "XRPUSDT": "XRP-USD", "BNBUSDT": "BNB-USD",
    "SOLUSDT": "SOL-USD", "DOGEUSDT": "DOGE-USD", "ADAUSDT": "ADA-USD", "AVAXUSDT": "AVAX-USD",
    "XLMUSDT": "XLM-USD", "SHIBUSDT": "SHIB-USD", "LINKUSDT": "LINK-USD",
    "WAXPUSDT": "WAXP-USD", "PAXGUSDT": "PAXG-USD"
}

# **Obtener la apertura mensual de los últimos 6 meses**
def get_monthly_open(symbol):
    crypto = yf.Ticker(symbol)
    hist = crypto.history(period="6mo", interval="1mo")

    if hist.empty:
        print(f"No se encontraron datos para {symbol}")
        return []

    return list(zip(hist.index.strftime("%Y-%m"), hist["Open"].tolist()))  # Fecha y apertura

# **Obtener el precio actual**
def get_current_price(symbol):
    crypto = yf.Ticker(symbol)
    price = crypto.history(period="1d")["Close"].values

    if len(price) == 0:
        print(f"Error obteniendo el precio actual de {symbol}")
        return None

    return float(price[-1])

# **Obtener y filtrar datos**
filtered_data = []

for ticker, yahoo_symbol in symbols.items():
    monthly_opens = get_monthly_open(yahoo_symbol)
    current_price = get_current_price(yahoo_symbol)

    if current_price is None:
        continue

    for date, open_price in monthly_opens:
        rango = ((current_price - open_price) / open_price) * 100

        if abs(rango) <= 1:  # ±1%
            filtered_data.append([ticker, current_price, open_price, date, round(rango, 2)])

# **Crear DataFrame con los resultados**
df = pd.DataFrame(filtered_data, columns=["Symbol", "Current Price", "Monthly Open", "Fecha", "Rango (%)"])

# **Función para generar tabla HTML**
def generar_tabla_html(df):
    estilos = """
    <style>
        table {border-collapse: collapse; width: 100%; font-family: Arial;}
        th, td {border: 1px solid #ddd; padding: 10px; text-align: center;}
        th {background-color: #0073aa; color: white; font-weight: bold;}
    </style>
    """
    return estilos + df.to_html(index=False, escape=False)

# **Publicar en WordPress (Post 1343)**
post_id = "1343"
wordpress_url = f"https://www.estrategiaelite.com/wp-json/wp/v2/posts/{post_idERE}"

post_data = {
    "title": f"Aperturas Mensuales - {datetime.today().strftime('%Y-%m-%d')}",
    "content": generar_tabla_html(df)
}

response = requests.put(
    wordpress_url, 
    json=post_data, 
    auth=(os.getenv("WORDPRESS_USER"), os.getenv("WORDPRESS_PASSWORD"))
)

if response.status_code == 200:
    print("✅ ¡Publicación actualizada en WordPress!")
else:
    print(f"❌ Error al actualizar la publicación: {response.status_code} - {response.text}")

