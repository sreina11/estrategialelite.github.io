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
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import os

# --- Configuración ---
WORDPRESS_URL = "https://www.estrategiaelite.com/wp-json/wp/v2"
POST_ID_OSCILADORES = 1334
POST_ID_RSI = 1326
POST_ID_MEDIAS_MOVILES = 2617
POST_ID_DESTINO = 1366
USERNAME = os.getenv("WORDPRESS_USER")
PASSWORD = os.getenv("WORDPRESS_PASSWORD")

# --- Función para obtener contenido HTML de un post ---
def obtener_contenido_post(post_id):
    url = f"{WORDPRESS_URL}/posts/{post_id}"
    response = requests.get(url, auth=(USERNAME, PASSWORD))
    if response.status_code == 200:
        return response.json().get("content", {}).get("rendered", "")
    else:
        print(f"❌ Error al obtener el post {post_id}: {response.status_code}")
        return ""

# --- Extraer la primera tabla HTML como DataFrame ---
def extraer_dataframe(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find("table")
    if table:
        return pd.read_html(str(table))[0]
    else:
        return pd.DataFrame()

# --- Obtener y limpiar los datos fuente ---
df_osciladores = extraer_dataframe(obtener_contenido_post(POST_ID_OSCILADORES))
df_rsi = extraer_dataframe(obtener_contenido_post(POST_ID_RSI))
df_medias = extraer_dataframe(obtener_contenido_post(POST_ID_MEDIAS_MOVILES))

# --- Validación ---
if df_osciladores.empty or df_rsi.empty or df_medias.empty:
    print("❌ Uno o más DataFrames están vacíos. Revisa los posts fuente.")
    exit()

# --- Limpieza básica ---
for df in [df_osciladores, df_rsi, df_medias]:
    df.columns = [col.strip() for col in df.columns]
    for col in df.columns[1:]:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# --- Identificar condiciones Estocástico ---
condiciones_stoch = []
for _, row in df_osciladores.iterrows():
    ticker = row["Ticker"]
    for col in df_osciladores.columns[1:]:
        if "Stoch" in col:
            val = row[col]
            if pd.notnull(val):
                if val >= 80:
                    condiciones_stoch.append({"Ticker": ticker, "Oscilador": col, "Valor": val, "Condición": "Sobrecomprado"})
                elif val <= 20:
                    condiciones_stoch.append({"Ticker": ticker, "Oscilador": col, "Valor": val, "Condición": "Sobrevendido"})

df_stoch = pd.DataFrame(condiciones_stoch)

# --- Identificar condiciones RSI ---
condiciones_rsi = []
for _, row in df_rsi.iterrows():
    ticker = row["Ticker"]
    for col in df_rsi.columns[1:]:
        val = row[col]
        if pd.notnull(val):
            if val >= 70:
                condiciones_rsi.append({"Ticker": ticker, "Oscilador": col, "Valor": val, "Condición": "Sobrecomprado"})
            elif val <= 30:
                condiciones_rsi.append({"Ticker": ticker, "Oscilador": col, "Valor": val, "Condición": "Sobrevendido"})

df_rsi_cond = pd.DataFrame(condiciones_rsi)

# --- Filtrar medias móviles ±1% ---
df_medias_filtrado = df_medias.copy()
for col in df_medias.columns[1:]:
    df_medias_filtrado[col] = df_medias[col].apply(lambda x: x if pd.notnull(x) and abs(x) <= 1 else None)

# --- Función para obtener confluencias ---
def obtener_confluencias(df_osc, tipo="Estocástico"):
    confluencias = []
    for _, osc in df_osc.iterrows():
        ticker = osc["Ticker"]
        if ticker in df_medias_filtrado["Ticker"].values:
            row_ma = df_medias_filtrado[df_medias_filtrado["Ticker"] == ticker]
            for col in df_medias_filtrado.columns[1:]:
                val_ma = row_ma[col].values[0]
                if pd.notnull(val_ma):
                    confluencias.append({
                        "Ticker": ticker,
                        f"{tipo}": f"{osc['Oscilador']} = {osc['Valor']:.2f} ({osc['Condición']})",
                        "Media Móvil": f"{col} = {val_ma:.2f} (≈1%) ✅"
                    })
    return pd.DataFrame(confluencias)

df_confluencias_stoch = obtener_confluencias(df_stoch, "Estocástico")
df_confluencias_rsi = obtener_confluencias(df_rsi_cond, "RSI")

# --- Generar HTML limpio ---
def generar_html(df, titulo):
    estilo = """
    <style>
    table {border-collapse: collapse; width: 100%; font-family: Arial;}
    th, td {border: 1px solid #ddd; padding: 8px; text-align: center;}
    th {background-color: #0073aa; color: white;}
    </style>
    """
    return f"<h3>{titulo}</h3>" + estilo + df.to_html(index=False)

# --- Armar contenido final ---
contenido_final = ""
if not df_confluencias_stoch.empty:
    contenido_final += generar_html(df_confluencias_stoch, "Estocástico + Media Móvil")
if not df_confluencias_rsi.empty:
    contenido_final += generar_html(df_confluencias_rsi, "RSI + Media Móvil")
if df_confluencias_stoch.empty and df_confluencias_rsi.empty:
    contenido_final = "<p>No hay confluencias detectadas.</p>"

# --- Actualizar el post en WordPress ---
url_actualizar = f"{WORDPRESS_URL}/posts/{POST_ID_DESTINO}"
datos_post = {
    "title": f"Confluencias MA + Osciladores - {datetime.today().strftime('%Y-%m-%d')}",
    "content": contenido_final
}

respuesta = requests.put(url_actualizar, json=datos_post, auth=(USERNAME, PASSWORD))
if respuesta.status_code == 200:
    print("✅ ¡Publicación actualizada en WordPress!")
else:
    print(f"❌ Error al actualizar la publicación: {respuesta.status_code} - {respuesta.text}")

# Medias mobiles Precios

import requests
from tradingview_ta import TA_Handler, Interval
import pandas as pd
import datetime
import os

# ----------- Configuración de activos y temporalidades -----------
activos = {
    "ETHUSDT": "BINANCE", "XRPUSDT": "BINANCE", "BNBUSDT": "BINANCE",
    "SOLUSDT": "BINANCE", "DOGEUSDT": "BINANCE", "ADAUSDT": "BINANCE",
    "AVAXUSDT": "BINANCE", "XLMUSDT": "BINANCE", "BTCUSDT": "BINANCE",
    "SHIBUSDT": "BINANCE", "LINKUSDT": "BINANCE", "ARPAUSDT": "BINANCE",
    "WAXPUSDT": "BINANCE", "PAXGUSDT": "BINANCE"
}

temporalidades = {
    "4H": Interval.INTERVAL_4_HOURS,  # 🔹 NUEVA TEMPORALIDAD 🔹
    "Diario": Interval.INTERVAL_1_DAY,
    "Semanal": Interval.INTERVAL_1_WEEK,
    "Mensual": Interval.INTERVAL_1_MONTH
}

# ----------- Obtener precios actuales de medias móviles -----------

def obtener_medias(ticker, exchange):
    resultado = {}
    for nombre_tf, intervalo in temporalidades.items():
        try:
            handler = TA_Handler(
                symbol=ticker,
                exchange=exchange,
                screener="crypto",
                interval=intervalo
            )
            analysis = handler.get_analysis()

            sma20 = analysis.indicators.get("SMA20") or analysis.indicators.get("EMA20")
            sma50 = analysis.indicators.get("SMA50") or analysis.indicators.get("EMA50")
            sma200 = analysis.indicators.get("SMA200") or analysis.indicators.get("EMA200")

            resultado[nombre_tf] = {
                "MA20": round(sma20, 4) if sma20 else "N/A",
                "MA50": round(sma50, 4) if sma50 else "N/A",
                "MA200": round(sma200, 4) if sma200 else "N/A"
            }
        except Exception as e:
            print(f"⚠️ Error con {ticker} en {nombre_tf}: {e}")
            resultado[nombre_tf] = {"MA20": "Err", "MA50": "Err", "MA200": "Err"}

    return resultado

# ----------- Recolectar todos los datos -----------

filas = []

for ticker, exchange in activos.items():
    datos = obtener_medias(ticker, exchange)
    filas.append([
        ticker,
        datos["4H"]["MA20"], datos["4H"]["MA50"], datos["4H"]["MA200"],  # 🔹 NUEVA TEMPORALIDAD 🔹
        datos["Diario"]["MA20"], datos["Diario"]["MA50"], datos["Diario"]["MA200"],
        datos["Semanal"]["MA20"], datos["Semanal"]["MA50"], datos["Semanal"]["MA200"],
        datos["Mensual"]["MA20"], datos["Mensual"]["MA50"], datos["Mensual"]["MA200"]
    ])

columnas = [
    "Ticker", "MA20_4H", "MA50_4H", "MA200_4H",  # 🔹 NUEVA TEMPORALIDAD 🔹
    "MA20_D", "MA50_D", "MA200_D",
    "MA20_W", "MA50_W", "MA200_W",
    "MA20_M", "MA50_M", "MA200_M"
]

df = pd.DataFrame(filas, columns=columnas)

# ----------- Tabla HTML para WordPress -----------

def tabla_html(df):
    estilo = """
    <style>
        table {border-collapse: collapse; width: 100%; font-family: Arial;}
        th, td {border: 1px solid #ccc; padding: 8px; text-align: center;}
        th {background-color: #222; color: white;}
    </style>
    """
    return estilo + df.to_html(index=False)

# ----------- Publicar en WordPress (POST ID 2647) -----------

wordpress_url = f"https://www.estrategiaelite.com/wp-json/wp/v2/posts/2647"

post_data = {
    "title": f"Precios de Medias Móviles - {datetime.date.today()}",
    "content": f"<h2>Medias Móviles por Temporalidad</h2>{tabla_html(df)}"
}

response = requests.put(
    wordpress_url,
    auth=(os.getenv("WORDPRESS_USER"), os.getenv("WORDPRESS_PASSWORD")),
    json=post_data
)

if response.status_code == 200:
    print("✅ ¡Post actualizado correctamente!")
else:
    print(f"❌ Error al publicar: {response.status_code} - {response.text}")

# **Función para obtener RSI y Estocástico desde TradingView**
def get_oscillator_data(asset, market):
    oscillators = {}
    for period_name, interval in intervals_osc.items():
        try:
            handler = TA_Handler(symbol=asset, exchange=market, screener="crypto", interval=interval)
            analysis = handler.get_analysis()
            rsi = analysis.indicators.get("RSI", None)
            stoch = analysis.indicators.get("Stoch.K", None)

            if rsi is not None:
                oscillators[f"RSI_{period_name}"] = round(rsi, 2)
            if stoch is not None:
                oscillators[f"Stoch_{period_name}"] = round(stoch, 2)
        except Exception:
            pass
    return oscillators

# **Filtrar confluencias**
filtered_confluences = []
for asset, market in assets.items():
    ma_200 = get_ma_data(asset, market, "SMA200")
    ma_50 = get_ma_data(asset, market, "SMA50")
    ma_20 = get_ma_data(asset, market, "SMA20")
    oscillators = get_oscillator_data(asset, market)

    def apply_colors(value, indicator):
        if value is None:
            return "<span style='color: gray;'>N/A</span>"
        if indicator == "RSI" and (value >= 70 or value <= 30):
            return f'<span style="color: {"red" if value >= 70 else "green"}; font-weight: bold;">{value:.2f}</span>'
        elif indicator == "Stoch" and (value >= 80 or value <= 20):
            return f'<span style="color: {"red" if value >= 80 else "green"}; font-weight: bold;">{value:.2f}</span>'
        return f'<span style="font-weight: bold;">{value:.2f}</span>'

    for ma_type, ma_data in {"MA200": ma_200, "MA50": ma_50, "MA20": ma_20}.items():
        for period, values in ma_data.items():
            if f"{ma_type}_{period}" in values:
                if any(oscillators.get(f"RSI_{p}", None) is not None and (oscillators[f"RSI_{p}"] <= 30 or oscillators[f"RSI_{p}"] >= 70) for p in intervals_osc.keys()) or \
                   any(oscillators.get(f"Stoch_{p}", None) is not None and (oscillators[f"Stoch_{p}"] <= 20 or oscillators[f"Stoch_{p}"] >= 80) for p in intervals_osc.keys()):
                    filtered_confluences.append([
                        values["Ticker"], values["Precio"], values[f"{ma_type}_{period}"], values[f"Rango_{period}"],
                        apply_colors(oscillators.get("Stoch_4H", None), "Stoch"), apply_colors(oscillators.get("Stoch_1D", None), "Stoch"),
                        apply_colors(oscillators.get("Stoch_1W", None), "Stoch"), apply_colors(oscillators.get("Stoch_1M", None), "Stoch"),
                        apply_colors(oscillators.get("RSI_4H", None), "RSI"), apply_colors(oscillators.get("RSI_1D", None), "RSI"),
                        apply_colors(oscillators.get("RSI_1W", None), "RSI"), apply_colors(oscillators.get("RSI_1M", None), "RSI"),
                    ])

df_confluences = pd.DataFrame(filtered_confluences, columns=[
    "Ticker", "Precio", "MA", "Rango", "Stoch_4H", "Stoch_1D", "Stoch_1W", "Stoch_1M", "RSI_4H", "RSI_1D", "RSI_1W", "RSI_1M"
])

# **Publicar en WordPress (Post 1366)**
wordpress_url = "https://www.estrategiaelite.com/wp-json/wp/v2/posts/1366"
post_data = {
    "title": f"Confluencias MA + Osciladores - {datetime.today().strftime('%Y-%m-%d')}",
    "content": df_confluences.to_html(index=False) if not df_confluences.empty else "<p>No hay confluencias.</p>"
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

# BANDAS DE BOLLINGER PRECIOS
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

    for nombre, intervalo in temporalidades.items():
        try:
            handler = TA_Handler(symbol=ticker, exchange=exchange, screener="crypto", interval=intervalo)
            analysis = handler.get_analysis()
            
            precios[nombre] = {
                "BB_UP": round(analysis.indicators["BB.upper"], 4),
                "BB_Low": round(analysis.indicators["BB.lower"], 4)
            }

        except Exception as e:
            print(f"Error en {ticker} - {nombre}: {e}")
            precios[nombre] = {"BB_UP": None, "BB_Low": None}

    return precios

# ----------- Recolectar datos en tiempo real -----------
bollinger_data = []

for ticker, exchange in activos.items():
    precios = analizar_ticker(ticker, exchange)
    
    bollinger_data.append([
        ticker,
        precios["Diario"]["BB_UP"], precios["Diario"]["BB_Low"],
        precios["Semanal"]["BB_UP"], precios["Semanal"]["BB_Low"],
        precios["Mensual"]["BB_UP"], precios["Mensual"]["BB_Low"]
    ])

# **Crear DataFrame con los resultados**
columnas = ["Ticker", "BB_UP_Diario", "BB_Low_Diario", "BB_UP_Semanal", "BB_Low_Semanal", "BB_UP_Mensual", "BB_Low_Mensual"]
df_bollinger = pd.DataFrame(bollinger_data, columns=columnas)

# **Publicar en WordPress (Post 2642)**
post_id = "2642"
wordpress_url = f"https://www.estrategiaelite.com/wp-json/wp/v2/posts/{post_id}"

# **Generar tabla HTML**
def generar_tabla_html(df):
    estilos = """
    <style>
        table {border-collapse: collapse; width: 100%; font-family: Arial;}
        th, td {border: 1px solid #ddd; padding: 10px; text-align: center;}
        th {background-color: #0073aa; color: white; font-weight: bold;}
    </style>
    """
    return estilos + df.to_html(index=False, escape=False)

# **Publicar en WordPress**
post_data = {
    "title": f"Bandas de Bollinger Últimos Datos - {datetime.datetime.today().strftime('%Y-%m-%d')}",
    "content": f"<h2>Precios de Bandas de Bollinger</h2>{generar_tabla_html(df_bollinger)}"
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

# **Funciones para calcular RSI y Estocástico**
def calculate_rsi(df, period=14):
    if df.empty:
        return None
    delta = df["Close"].diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return round(float(rsi.iloc[-1]), 2) if not rsi.empty else None

def calculate_stoch(df, period=14):
    if df.empty:
        return None
    lowest_low = df["Low"].rolling(window=period).min()
    highest_high = df["High"].rolling(window=period).max()
    stoch = ((df["Close"] - lowest_low) / (highest_high - lowest_low)) * 100
    return round(float(stoch.iloc[-1]), 2) if not stoch.empty else None

# **Función para aplicar colores**
def aplicar_colores(valor, tipo):
    if valor is not None:
        if tipo == "RSI":
            if valor >= 70:
                return f'<span style="color: red; font-weight: bold;">{valor:.2f}</span>'
            elif valor <= 30:
                return f'<span style="color: green; font-weight: bold;">{valor:.2f}</span>'
        elif tipo == "STOCH":
            if valor >= 80:
                return f'<span style="color: red; font-weight: bold;">{valor:.2f}</span>'
            elif valor <= 20:
                return f'<span style="color: green; font-weight: bold;">{valor:.2f}</span>'
    return f'<span style="font-weight: bold;">{valor:.2f}</span>'

# **Obtener y filtrar datos**
filtered_rsi = []
filtered_stoch = []

for ticker, yahoo_symbol in symbols.items():
    monthly_opens = get_monthly_open(yahoo_symbol)
    current_price = get_current_price(yahoo_symbol)

    if current_price is None:
        continue

    for date, open_price in monthly_opens:
        rango = ((current_price - open_price) / open_price) * 100

        if abs(rango) <= 1:  # ±1%
            df_4h = yf.download(yahoo_symbol, period="7d", interval="4h")
            df_daily = yf.download(yahoo_symbol, period="6mo", interval="1d")
            df_weekly = yf.download(yahoo_symbol, period="3y", interval="1wk")

            rsi_4h = calculate_rsi(df_4h)
            rsi_d = calculate_rsi(df_daily)
            rsi_w = calculate_rsi(df_weekly)

            stoch_4h = calculate_stoch(df_4h)
            stoch_d = calculate_stoch(df_daily)
            stoch_w = calculate_stoch(df_weekly)

            # **Filtrar activos con RSI extremo**
            if rsi_4h is not None and rsi_d is not None and rsi_w is not None:
                if rsi_4h <= 30 or rsi_4h >= 70 or rsi_d <= 30 or rsi_d >= 70 or rsi_w <= 30 or rsi_w >= 70:
                    filtered_rsi.append([ticker, current_price, open_price, date, round(rango, 2),
                                         aplicar_colores(rsi_4h, "RSI"), aplicar_colores(rsi_d, "RSI"), aplicar_colores(rsi_w, "RSI")])

            # **Filtrar activos con Estocástico extremo**
            if stoch_4h is not None and stoch_d is not None and stoch_w is not None:
                if stoch_4h <= 20 or stoch_4h >= 80 or stoch_d <= 20 or stoch_d >= 80 or stoch_w <= 20 or stoch_w >= 80:
                    filtered_stoch.append([ticker, current_price, open_price, date, round(rango, 2),
                                           aplicar_colores(stoch_4h, "STOCH"), aplicar_colores(stoch_d, "STOCH"), aplicar_colores(stoch_w, "STOCH")])

# **Crear DataFrames con los resultados**
df_rsi = pd.DataFrame(filtered_rsi, columns=["Symbol", "Current Price", "Monthly Open", "Fecha", "Rango (%)", "RSI_4H", "RSI_Diario", "RSI_Semanal"])
df_stoch = pd.DataFrame(filtered_stoch, columns=["Symbol", "Current Price", "Monthly Open", "Fecha", "Rango (%)", "STOCH_4H", "STOCH_Diario", "STOCH_Semanal"])

# **Publicar en WordPress (Post 1343)**
post_id = "1343"
wordpress_url = f"https://www.estrategiaelite.com/wp-json/wp/v2/posts/{post_id}"

# **Generar tabla HTML**
def generar_tabla_html(df):
    estilos = """
    <style>
        table {border-collapse: collapse; width: 100%; font-family: Arial;}
        th, td {border: 1px solid #ddd; padding: 10px; text-align: center;}
        th {background-color: #0073aa; color: white; font-weight: bold;}
    </style>
    """
    return estilos + df.to_html(index=False, escape=False)

# **Publicar en WordPress**
post_data = {
    "title": f"Aperturas Mensuales con RSI y Estocástico - {datetime.today().strftime('%Y-%m-%d')}",
    "content": f"<h2>APERTURA + RSI</h2>{generar_tabla_html(df_rsi)}<h2>APERTURA + STOCH</h2>{generar_tabla_html(df_stoch)}"
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

# APERTURAS PRECIO 8 MESES
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import requests
import os  # Para manejar variables de entorno
from requests.auth import HTTPBasicAuth

# **Lista de criptomonedas**
symbols = [
    "BTCUSDT", "ETHUSDT", "XRPUSDT", "BNBUSDT", "SOLUSDT", "DOGEUSDT", "ADAUSDT",
    "AVAXUSDT", "XLMUSDT", "HYPEUSDT", "SHIBUSDT", "LINKUSDT", "SUIUSDT",
    "WAXPUSDT", "PAXGUSDT"
]

# **Mapeo de símbolos para Yahoo Finance**
symbol_mapping = {symbol: symbol.replace("USDT", "-USD") for symbol in symbols}

# **Obtener los precios de apertura de los últimos 8 meses**
def get_monthly_open_prices(symbol):
    crypto = yf.Ticker(symbol_mapping[symbol])
    hist = crypto.history(period="8mo", interval="1mo")

    if hist.empty:
        print(f"No se encontraron datos para {symbol}")
        return []

    return list(hist["Open"].tolist())  # Lista de precios de apertura

# **Obtener las fechas de los últimos 8 meses**
crypto_example = yf.Ticker(list(symbol_mapping.values())[0])  # Tomamos cualquier cripto como ejemplo
hist_dates = crypto_example.history(period="8mo", interval="1mo").index.strftime("%Y-%m")

# **Construir el DataFrame**
data = {}

for ticker in symbols:
    open_prices = get_monthly_open_prices(ticker)
    if open_prices:
        data[ticker] = open_prices
    else:
        data[ticker] = [None] * len(hist_dates)  # Si no hay datos, llena con valores vacíos

df_openings = pd.DataFrame(data, index=hist_dates).T

# **Publicar en WordPress (Post 2635)**
post_id = "2635"
wordpress_url = f"https://www.estrategiaelite.com/wp-json/wp/v2/posts/{post_id}"

# **Generar tabla HTML**
def generar_tabla_html(df):
    estilos = """
    <style>
        table {border-collapse: collapse; width: 100%; font-family: Arial;}
        th, td {border: 1px solid #ddd; padding: 10px; text-align: center;}
        th {background-color: #0073aa; color: white; font-weight: bold;}
    </style>
    """
    return estilos + df.to_html(index=False, escape=False)

# **Publicar en WordPress**
post_data = {
    "title": f"Aperturas Mensuales Últimos 8 Meses - {datetime.today().strftime('%Y-%m-%d')}",
    "content": f"<h2>Aperturas Mensuales</h2>{generar_tabla_html(df_openings)}"
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


