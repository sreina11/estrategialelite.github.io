#------------------------------------ FOREX Y ORO --------------------------------------------
# ⚠️ Instalar librerías necesarias (si no están instaladas)
import requests
from tradingview_ta import TA_Handler, Interval
import pandas as pd

# **Lista de activos actualizada con DXY, Oro y Brent**
activos = {
    "USDJPY": "FX",
    "USDCOP": "FX",
    "USDCAD": "FX",
    "USDCHF": "FX",
    "GBPUSD": "FX",
    "GBPJPY": "FX",
    "EURAUD": "FX",
    "EURUSD": "FX",
    "EURJPY": "FX",
    "EURGBP": "FX",
    "AUDUSD": "FX",
    "AUDJPY": "FX",
    "NZDUSD": "FX",
    "CHFJPY": "FX",
    "CADJPY": "FX",
    "CADCHF": "FX",
    "XAUUSD": "OANDA",   # ✅ Oro con exchange correcto
    "DXY": "TVC",        # ✅ Índice del dólar (US Dollar Index)
}

# **Temporalidades**
temporalidades = {
    "RSI_4H": Interval.INTERVAL_4_HOURS,
    "RSI_1D": Interval.INTERVAL_1_DAY,
    "RSI_1W": Interval.INTERVAL_1_WEEK,
    "RSI_1M": Interval.INTERVAL_1_MONTH
}

# **Almacena resultados**
data = []

for activo, mercado in activos.items():
    fila = {"Ticker": activo}
    for nombre_columna, intervalo in temporalidades.items():
        try:
            handler = TA_Handler(
                symbol=activo,
                exchange=mercado,
                screener="forex" if mercado == "FX" else "cfd",
                interval=intervalo
            )
            rsi_valor = handler.get_analysis().indicators.get("RSI")
            fila[nombre_columna] = rsi_valor
        except:
            fila[nombre_columna] = None
    data.append(fila)

# **Crear DataFrame**
df_rsi = pd.DataFrame(data)

# **Convertir a numérico y redondear**
for col in temporalidades.keys():
    df_rsi[col] = pd.to_numeric(df_rsi[col], errors="coerce").round(2)

# **Mostrar datos antes del filtrado**
print("📊 Datos antes del filtro:")
print(df_rsi)

# **Filtro corregido: RSI ≤ 30 o ≥ 70 en cualquiera de las temporalidades**
df_filtrado = df_rsi[
    (df_rsi["RSI_4H"] <= 30) | (df_rsi["RSI_4H"] >= 70) |
    (df_rsi["RSI_1D"] <= 30) | (df_rsi["RSI_1D"] >= 70) |
    (df_rsi["RSI_1W"] <= 30) | (df_rsi["RSI_1W"] >= 70) |
    (df_rsi["RSI_1M"] <= 30) | (df_rsi["RSI_1M"] >= 70)
]

# **Mostrar datos después del filtrado**
print("\n📊 Datos después del filtro:")
print(df_filtrado if not df_filtrado.empty else "No hay activos con RSI extremo.")

# POST RSI FOREX
import requests
import datetime
import pandas as pd
import os  # Para manejar credenciales de WordPress desde secrets

# ⚠️ **Reemplaza el ID con el que obtuviste en la publicación inicial**
post_id = "1142"  # ⚠️ Usa el ID correcto generado antes

# **URL de la API para actualizar el post**
wordpress_url = f"https://estrategiaelite.com/wp-json/wp/v2/posts/{post_id}"

# **Función para aplicar colores al RSI**
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
        th {border: 1px solid #ddd; padding: 10px; text-align: left; background-color: #0073aa; color: white; font-weight: bold;}
        td {border: 1px solid #ddd; padding: 10px; text-align: center;}
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
    auth=(os.getenv("WORDPRESS_USER"), os.getenv("WORDPRESS_PASSWORD"))  # 🔒 Seguridad en GitHub Secrets
)

# **Verificar si la actualización fue exitosa**
if response.status_code == 200:
    print("✅ ¡Publicación de RSI actualizada exitosamente en WordPress!")
else:
    print(f"❌ Error al actualizar RSI: {response.status_code}, {response.text}")

# ESTOCASTICO FOREX

# **Importar librerías**
from tradingview_ta import TA_Handler, Interval
import pandas as pd

# **Lista de activos actualizada con DXY, Oro y Forex**
activos = {
    "USDJPY": "FX",
    "USDCOP": "FX",
    "USDCAD": "FX",
    "USDCHF": "FX",
    "GBPUSD": "FX",
    "GBPJPY": "FX",
    "EURAUD": "FX",
    "EURUSD": "FX",
    "EURJPY": "FX",
    "EURGBP": "FX",
    "AUDUSD": "FX",
    "AUDJPY": "FX",
    "NZDUSD": "FX",
    "CHFJPY": "FX",
    "CADJPY": "FX",
    "CADCHF": "FX",
    "XAUUSD": "OANDA",   # ✅ Oro con exchange correcto
    "DXY": "TVC"         # ✅ Índice del dólar (US Dollar Index)
}

# **Temporalidades**
temporalidades = {
    "Stoch_4H": Interval.INTERVAL_4_HOURS,
    "Stoch_1D": Interval.INTERVAL_1_DAY,
    "Stoch_1W": Interval.INTERVAL_1_WEEK,
    "Stoch_1M": Interval.INTERVAL_1_MONTH
}

# **Almacenar resultados**
data = []

for activo, mercado in activos.items():
    fila = {"Ticker": activo}
    for nombre_columna, intervalo in temporalidades.items():
        try:
            handler = TA_Handler(
                symbol=activo,
                exchange=mercado,
                screener="forex" if mercado == "FX" else "cfd",
                interval=intervalo
            )
            stoch_valor = handler.get_analysis().indicators.get("Stoch.K")  # ⚠️ Estocástico %K
            fila[nombre_columna] = stoch_valor
        except:
            fila[nombre_columna] = None
    data.append(fila)

# **Crear DataFrame**
df_stoch = pd.DataFrame(data)

# **Convertir a numérico y redondear**
for col in temporalidades.keys():
    df_stoch[col] = pd.to_numeric(df_stoch[col], errors="coerce").round(2)

# **Mostrar datos antes del filtrado**
print("📊 Datos antes del filtro:")
print(df_stoch)

# **Filtrar activos con Estocástico sobrecompra (≥80) o sobreventa (≤20)**
df_filtrado = df_stoch[
    (df_stoch["Stoch_4H"] <= 20) | (df_stoch["Stoch_4H"] >= 80) |
    (df_stoch["Stoch_1D"] <= 20) | (df_stoch["Stoch_1D"] >= 80) |
    (df_stoch["Stoch_1W"] <= 20) | (df_stoch["Stoch_1W"] >= 80) |
    (df_stoch["Stoch_1M"] <= 20) | (df_stoch["Stoch_1M"] >= 80)
]

# **Mostrar datos después del filtrado**
print("\n📊 Activos con Estocástico en zona extrema (≤20 o ≥80):")
print(df_filtrado if not df_filtrado.empty else "No hay activos en zona extrema.")

#POST ESTOCASTICO FOREX
# ⚠️ Instalar librerías necesarias
import requests
import datetime
import pandas as pd
import os  # Para manejar credenciales de WordPress desde secretos

# ⚠️ **Reemplaza con el ID del post que ya generaste**
post_id = "1149"  

# **URL de la API para actualizar el post**
wordpress_url = f"https://estrategiaelite.com/wp-json/wp/v2/posts/{post_id}"

# **Función para aplicar colores al Estocástico**
def aplicar_colores(valor):
    """Aplica colores y negrita basados en el valor de Stoch.K."""
    if pd.notna(valor):  # Evita errores con valores nulos
        if valor >= 80:
            return f'<span style="color: red; font-weight: bold;">{valor}</span>'  # Zona de sobrecompra
        elif valor <= 20:
            return f'<span style="color: green; font-weight: bold;">{valor}</span>'  # Zona de sobreventa
    return f'<span style="font-weight: bold;">{valor}</span>'  # Negrita sin color

# ✅ **Tomar el DataFrame original (`df_stoch`) sin modificaciones**
df_coloreado = df_stoch.copy()

# **Aplicar colores al DataFrame**
for col in df_stoch.columns[1:]:  # ✅ No modificar la estructura, solo aplicar formato visual
    df_coloreado[col] = df_coloreado[col].apply(aplicar_colores)

# **Diseño de la tabla en HTML con estilos**
def generar_tabla_html(df):
    estilos = """
    <style>
        table {border-collapse: collapse; width: 100%; font-family: Arial;}
        th {border: 1px solid #ddd; padding: 10px; text-align: left; background-color: #0073aa; color: white; font-weight: bold;}
        td {border: 1px solid #ddd; padding: 10px; text-align: center;}
        tr:nth-child(even) {background-color: #f2f2f2;}
        tr:hover {background-color: #ddd;}
    </style>
    """
    return estilos + df.to_html(index=False, escape=False)

# **Datos de la actualización**
post_data = {
    "title": f"Oscilador Estocástico - Actualización {datetime.datetime.now().strftime('%Y-%m-%d')}",
    "content": generar_tabla_html(df_coloreado)
}

# **Ejecutar la solicitud PUT para actualizar el post existente**
response = requests.put(
    wordpress_url,
    json=post_data,
    auth=(os.getenv("WORDPRESS_USER"), os.getenv("WORDPRESS_PASSWORD"))  # 🔒 Seguridad en GitHub Secrets
)

# **Verificar si la actualización fue exitosa**
if response.status_code == 200:
    print("✅ ¡Publicación del Oscilador Estocástico actualizada exitosamente en WordPress!")
else:
    print(f"❌ Error al actualizar en WordPress: {response.status_code}, {response.text}")

# CONFLUENCIAS BB RSI ESTOC

import requests
from tradingview_ta import TA_Handler, Interval
import pandas as pd
import datetime
import os

# --- Activos ---
activos = {
    "USDJPY": "FX", "USDCOP": "FX", "USDCAD": "FX", "USDCHF": "FX",
    "GBPUSD": "FX", "GBPJPY": "FX", "EURAUD": "FX", "EURUSD": "FX",
    "EURJPY": "FX", "EURGBP": "FX", "AUDUSD": "FX", "AUDJPY": "FX",
    "NZDUSD": "FX", "CHFJPY": "FX", "CADJPY": "FX", "CADCHF": "FX",
    "XAUUSD": "OANDA", "DXY": "TVC"
}

# --- Temporalidades ---
temporalidades = {
    "4H": Interval.INTERVAL_4_HOURS,
    "Diario": Interval.INTERVAL_1_DAY,
    "Semanal": Interval.INTERVAL_1_WEEK,
    "Mensual": Interval.INTERVAL_1_MONTH
}

# --- Diccionarios para almacenar las confluencias ---
confluencias_rsi = {"4H": [], "Diario": [], "Semanal": [], "Mensual": []}
confluencias_stoch = {"4H": [], "Diario": [], "Semanal": [], "Mensual": []}

# --- Recolectar y procesar datos ---
for activo, mercado in activos.items():
    datos = {}
    for periodo_nombre, intervalo in temporalidades.items():
        try:
            handler = TA_Handler(
                symbol=activo,
                exchange=mercado,
                screener="forex" if mercado == "FX" else "cfd",
                interval=intervalo
            )
            analysis = handler.get_analysis()
            precio = analysis.indicators.get("close", None)
            bb_upper = analysis.indicators.get("BB.upper", None)
            bb_lower = analysis.indicators.get("BB.lower", None)
            rsi = analysis.indicators.get("RSI", None)
            stoch = analysis.indicators.get("Stoch.K", None)

            if precio is not None:
                precio = round(precio, 2) if activo in ["XAUUSD", "DXY"] else round(precio, 4)

            datos[periodo_nombre] = {
                "Precio": precio,
                "BB.upper": bb_upper,
                "BB.lower": bb_lower,
                "RSI": rsi,
                "Stoch.K": stoch
            }

        except Exception as e:
            print(f"❌ Error con {activo} ({periodo_nombre}): {e}")

    # --- Evaluar confluencias RSI ---
    for tf in ["4H", "Diario", "Semanal", "Mensual"]:
        try:
            datos_tf = datos.get(tf, {})
            bb_upper = datos_tf.get("BB.upper")
            bb_lower = datos_tf.get("BB.lower")
            precio = datos_tf.get("Precio")
            rsi_tf = datos_tf.get("RSI")
            rsi_4h = datos.get("4H", {}).get("RSI")

            if all(v is not None for v in [precio, bb_upper, bb_lower, rsi_tf, rsi_4h]):
                if (precio >= bb_upper or precio <= bb_lower) and (rsi_tf >= 70 or rsi_tf <= 30 or rsi_4h >= 70 or rsi_4h <= 30):
                    confluencias_rsi[tf].append({
                        "Ticker": activo,
                        "Precio actual": precio,
                        "Precio BB_UP": round(bb_upper, 4),
                        "Precio BB_Low": round(bb_lower, 4),
                        "RSI_4H": round(rsi_4h, 2),
                        "RSI_Diario": round(datos.get("Diario", {}).get("RSI", 0), 2),
                        "RSI_Semanal": round(datos.get("Semanal", {}).get("RSI", 0), 2),
                        "RSI_Mensual": round(datos.get("Mensual", {}).get("RSI", 0), 2)
                    })
        except:
            pass

    # --- Evaluar confluencias Estocástico ---
    for tf in ["4H", "Diario", "Semanal", "Mensual"]:
        try:
            datos_tf = datos.get(tf, {})
            bb_upper = datos_tf.get("BB.upper")
            bb_lower = datos_tf.get("BB.lower")
            precio = datos_tf.get("Precio")
            stoch_tf = datos_tf.get("Stoch.K")
            stoch_4h = datos.get("4H", {}).get("Stoch.K")

            if all(v is not None for v in [precio, bb_upper, bb_lower, stoch_tf, stoch_4h]):
                if (precio >= bb_upper or precio <= bb_lower) and (stoch_tf >= 80 or stoch_tf <= 20 or stoch_4h >= 80 or stoch_4h <= 20):
                    confluencias_stoch[tf].append({
                        "Ticker": activo,
                        "Precio actual": precio,
                        "Precio BB_UP": round(bb_upper, 4),
                        "Precio BB_Low": round(bb_lower, 4),
                        "STOCH_4H": round(stoch_4h, 2),
                        "STOCH_Diario": round(datos.get("Diario", {}).get("Stoch.K", 0), 2),
                        "STOCH_Semanal": round(datos.get("Semanal", {}).get("Stoch.K", 0), 2),
                        "STOCH_Mensual": round(datos.get("Mensual", {}).get("Stoch.K", 0), 2)
                    })
        except:
            pass

# ------------------ Generar contenido HTML ------------------

def aplicar_formato(valor, indicador):
    try:
        if indicador == "RSI":
            if valor <= 30:
                return f'<span style="color: green; font-weight: bold;">{valor}</span>'
            elif valor >= 70:
                return f'<span style="color: red; font-weight: bold;">{valor}</span>'
        elif indicador == "STOCH":
            if valor <= 20:
                return f'<span style="color: green; font-weight: bold;">{valor}</span>'
            elif valor >= 80:
                return f'<span style="color: red; font-weight: bold;">{valor}</span>'
        return f'{valor}'
    except:
        return valor

def generar_tabla_html(lista_dict, tipo):
    if not lista_dict:
        return "<p>No hay confluencias.</p>"
    df = pd.DataFrame(lista_dict)

    # Aplicar formato a las columnas de osciladores
    if tipo == "RSI":
        for col in ["RSI_4H", "RSI_Diario", "RSI_Semanal", "RSI_Mensual"]:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: aplicar_formato(x, "RSI"))
    elif tipo == "STOCH":
        for col in ["STOCH_4H", "STOCH_Diario", "STOCH_Semanal", "STOCH_Mensual"]:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: aplicar_formato(x, "STOCH"))

    estilos = """
    <style>
        table {border-collapse: collapse; width: 100%; font-family: Arial;}
        th, td {border: 1px solid #ddd; padding: 10px; text-align: center;}
        th {background-color: #0073aa; color: white;}
        tr:nth-child(even) {background-color: #f2f2f2;}
    </style>
    """
    return estilos + df.to_html(index=False, escape=False)

def construir_seccion(nombre, data_dict, tipo):
    html = ""
    for tf in ["4H", "Diario", "Semanal", "Mensual"]:
        html += f"<h3>{tf}</h3>"
        html += generar_tabla_html(data_dict[tf], tipo)
    return html

# ------------------ Publicar en WordPress ------------------

contenido_post = f"""
<h4>Confluencias de Osciladores y Bandas de Bollinger – {datetime.datetime.now().strftime('%Y-%m-%d')}</h4>
<h2>Bandas de Bollinger y RSI</h2>
{construir_seccion("Bandas de Bollinger y RSI", confluencias_rsi, "RSI")}
<br>
<h2>Bandas de Bollinger y Estocástico</h2>
{construir_seccion("Bandas de Bollinger y Estocástico", confluencias_stoch, "STOCH")}
"""

wordpress_url = "https://estrategiaelite.com/wp-json/wp/v2/posts/1151"

post_data = {
    "title": f"Confluencias de Osciladores y Bandas de Bollinger – {datetime.datetime.now().strftime('%Y-%m-%d')}",
    "content": contenido_post
}

response = requests.put(
    wordpress_url,
    json=post_data,
    auth=(os.getenv("WORDPRESS_USER"), os.getenv("WORDPRESS_PASSWORD"))
)

if response.status_code == 200:
    print("✅ ¡Publicación actualizada exitosamente en WordPress!")
else:
    print(f"❌ Error al actualizar en WordPress: {response.status_code}, {response.text}")

# medias mobiles Precio y Rango

import yfinance as yf
import pandas as pd
import requests
import os
import datetime

# Activos (sin USDCOP)
tickers = [
    "JPY=X",     # USDJPY
    "CAD=X",     # USDCAD
    "CHF=X",     # USDCHF
    "GBPUSD=X",  # GBPUSD
    "GBPJPY=X",  # GBPJPY
    "EURAUD=X",  # EURAUD
    "EURUSD=X",  # EURUSD
    "EURJPY=X",  # EURJPY
    "EURGBP=X",  # EURGBP
    "AUDUSD=X",  # AUDUSD
    "AUDJPY=X",  # AUDJPY
    "NZDUSD=X",  # NZDUSD
    "CHFJPY=X",  # CHFJPY
    "CADJPY=X",  # CADJPY
    "CADCHF=X",  # CADCHF
    "XAUUSD=X",  # Oro vs USD
    "DX-Y.NYB"   # DXY
]

# Calcular el % de diferencia entre precio y media móvil
def pct_diff(price, ma):
    return round(((price - ma) / ma) * 100, 2) if price and ma else None

# Función para obtener medias móviles en la temporalidad dada
def get_ma_data(ticker, interval, label):
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period="max", interval=interval, auto_adjust=True)
        hist = hist.dropna(subset=["Close"])

        close = hist['Close'].iloc[-1] if not hist.empty else None
        ma20 = hist['Close'].rolling(window=20).mean().iloc[-1] if len(hist) >= 20 else None
        ma50 = hist['Close'].rolling(window=50).mean().iloc[-1] if len(hist) >= 50 else None
        ma200 = hist['Close'].rolling(window=200).mean().iloc[-1] if len(hist) >= 200 else None

        return pd.Series({
            'Ticker': ticker,
            'Precio Actual': round(close, 4) if close else None,
            f'{label}_MA20': round(ma20, 4) if ma20 else None,
            f'{label}_MA50': round(ma50, 4) if ma50 else None,
            f'{label}_MA200': round(ma200, 4) if ma200 else None,
            f'{label}_%vsMA20': pct_diff(close, ma20),
            f'{label}_%vsMA50': pct_diff(close, ma50),
            f'{label}_%vsMA200': pct_diff(close, ma200),
        })

    except Exception as e:
        print(f"⚠️ Error en {ticker} ({label}): {e}")
        return pd.Series({
            'Ticker': ticker,
            'Precio Actual': None,
            f'{label}_MA20': None,
            f'{label}_MA50': None,
            f'{label}_MA200': None,
            f'{label}_%vsMA20': None,
            f'{label}_%vsMA50': None,
            f'{label}_%vsMA200': None,
        })

# Obtener los dataframes por cada temporalidad
df_daily = pd.DataFrame([get_ma_data(ticker, "1d", "D") for ticker in tickers])
df_weekly = pd.DataFrame([get_ma_data(ticker, "1wk", "W") for ticker in tickers])
df_monthly = pd.DataFrame([get_ma_data(ticker, "1mo", "M") for ticker in tickers])

# Convertir a tabla HTML
def to_html_table(df, title):
    return f"<h2>{title}</h2>" + df.to_html(index=False, border=0, classes="wp-block-table", justify='center')

# Generar contenido HTML con la fecha de actualización
html_content = (
    f"<p>Última actualización: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}</p>"
    + to_html_table(df_daily, "Media Móvil Diaria")
    + to_html_table(df_weekly, "Media Móvil Semanal")
    + to_html_table(df_monthly, "Media Móvil Mensual")
)

# Actualizar el post en WordPress
post_id = "3071"
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

# MEDIAS CONFLUENCIAS MOVILES Y OSCILADORES 

import requests
import pandas as pd
from bs4 import BeautifulSoup
import os

# --- Diccionario de conversión de tickers ---
ticker_map = {
    "JPY=X": "USDJPY",
    "CAD=X": "USDCAD",
    "CHF=X": "USDCHF",
    "GBPUSD=X": "GBPUSD",
    "GBPJPY=X": "GBPJPY",
    "EURAUD=X": "EURAUD",
    "EURUSD=X": "EURUSD",
    "EURJPY=X": "EURJPY",
    "EURGBP=X": "EURGBP",
    "AUDUSD=X": "AUDUSD",
    "AUDJPY=X": "AUDJPY",
    "NZDUSD=X": "NZDUSD",
    "CHFJPY=X": "CHFJPY",
    "CADJPY=X": "CADJPY",
    "CADCHF=X": "CADCHF",
    "XAUUSD=X": "XAUUSD",
    "DX-Y.NYB": "DXY"
}

# --- URLs actualizadas ---
url_rsi = 'https://estrategiaelite.com/?p=1142'
url_stoch = 'https://estrategiaelite.com/oscilador-estocastico-publicacion-inicial-2025-05-18/'
url_ma = 'https://estrategiaelite.com/medias-mo-fx-rango-y-precios/'

# --- Función para extraer tablas ---
def get_tables_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return pd.read_html(str(soup))

# --- Descargar y asignar las tablas ---
rsi_tables = get_tables_from_url(url_rsi)
stoch_tables = get_tables_from_url(url_stoch)
ma_tables = get_tables_from_url(url_ma)

df_rsi = rsi_tables[0]
df_stoch = stoch_tables[0]

df_ma_daily = ma_tables[0]
df_ma_weekly = ma_tables[1]
df_ma_monthly = ma_tables[2]

# Convertir ticker_map en dataframe-friendly
df_ma_daily["Ticker"] = df_ma_daily["Ticker"].map(ticker_map)
df_ma_weekly["Ticker"] = df_ma_weekly["Ticker"].map(ticker_map)
df_ma_monthly["Ticker"] = df_ma_monthly["Ticker"].map(ticker_map)

# --- Función para verificar si el rango está dentro de ±1% ---
def is_near_ma(rango):
    return abs(rango) <= 1.0

rsi_resultados = []
stoch_resultados = []

# --- Unificar tickers ---
tickers = set(df_rsi['Ticker']) | set(df_stoch['Ticker']) | set(df_ma_daily['Ticker'])

# --- Procesar cada ticker ---
for ticker in tickers:
    if pd.isna(ticker):
        continue

    rsi_row = df_rsi[df_rsi['Ticker'] == ticker]
    stoch_row = df_stoch[df_stoch['Ticker'] == ticker]
    row_daily = df_ma_daily[df_ma_daily['Ticker'] == ticker]
    row_weekly = df_ma_weekly[df_ma_weekly['Ticker'] == ticker]
    row_monthly = df_ma_monthly[df_ma_monthly['Ticker'] == ticker]

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

    precio_actual = None
    for df in [row_daily, row_weekly, row_monthly]:
        if not df.empty and 'Precio Actual' in df.columns:
            try:
                precio_actual = float(df['Precio Actual'].values[0])
                break
            except:
                continue

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

# --- Convertir a HTML ---
html_rsi = "<h2>📊 Confluencias RSI + MA</h2>" + df_rsi_final.to_html(index=False, escape=False)
html_stoch = "<h2>📊 Confluencias Stoch + MA</h2>" + df_stoch_final.to_html(index=False, escape=False)
html_tabla = html_rsi + "<br><br>" + html_stoch

# --- Actualizar publicación en WordPress ---
wordpress_url = "https://estrategiaelite.com/wp-json/wp/v2/posts/1198"
titulo = "🔄 Actualización Confluencias Forex: Osciladores + Medias Móviles"

post_data = {
    "title": titulo,
    "content": html_tabla
}

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


# Aperturas Mensuales y Osciladores

import requests
import datetime
import pandas as pd
import os
from tradingview_ta import TA_Handler, Interval

# 📌 POST WORDPRESS
post_id = "1225"
wordpress_url = f"https://estrategiaelite.com/wp-json/wp/v2/posts/{post_id}"

# 📌 ACTIVOS A EVALUAR
activos = {
    "USDJPY": "FX", "USDCOP": "FX", "USDCAD": "FX", "USDCHF": "FX",
    "GBPUSD": "FX", "GBPJPY": "FX", "EURAUD": "FX", "EURUSD": "FX",
    "EURJPY": "FX", "EURGBP": "FX", "AUDUSD": "FX", "AUDJPY": "FX",
    "NZDUSD": "FX", "CHFJPY": "FX", "CADJPY": "FX", "CADCHF": "FX",
    "XAUUSD": "OANDA", "DXY": "TVC"
}

RANGO = 0.005  # ±0.5%

# 📌 FUNCIONES
def obtener_dato(handler, campo):
    try:
        return handler.get_analysis().indicators.get(campo)
    except:
        return None

def obtener_fecha_ultima_apertura():
    hoy = datetime.date.today()
    return datetime.date(hoy.year, hoy.month, 1).strftime("%Y-%m")

def obtener_indicadores(activo, exchange):
    resultado = {"RSI": {}, "Stoch": {}}
    intervalos = {
        "4H": Interval.INTERVAL_4_HOURS,
        "1D": Interval.INTERVAL_1_DAY,
        "1W": Interval.INTERVAL_1_WEEK,
        "1M": Interval.INTERVAL_1_MONTH,
    }

    for key, intervalo in intervalos.items():
        try:
            handler = TA_Handler(
                symbol=activo,
                exchange=exchange,
                screener="forex" if exchange == "FX" else "cfd",
                interval=intervalo
            )
            rsi = obtener_dato(handler, "RSI")
            stoch = obtener_dato(handler, "Stoch.K")
            resultado["RSI"][key] = round(rsi, 2) if rsi else None
            resultado["Stoch"][key] = round(stoch, 2) if stoch else None
        except:
            resultado["RSI"][key] = None
            resultado["Stoch"][key] = None

    return resultado

def obtener_precio_actual(activo, exchange):
    try:
        handler = TA_Handler(
            symbol=activo,
            exchange=exchange,
            screener="forex" if exchange == "FX" else "cfd",
            interval=Interval.INTERVAL_1_DAY
        )
        return handler.get_analysis().indicators.get("close")
    except:
        return None

def obtener_apertura_mensual(activo, exchange):
    try:
        handler = TA_Handler(
            symbol=activo,
            exchange=exchange,
            screener="forex" if exchange == "FX" else "cfd",
            interval=Interval.INTERVAL_1_MONTH
        )
        return handler.get_analysis().indicators.get("open")
    except:
        return None

# 📌 PROCESAMIENTO
filas = []
for activo, mercado in activos.items():
    apertura = obtener_apertura_mensual(activo, mercado)
    precio = obtener_precio_actual(activo, mercado)

    if apertura and precio and abs(precio - apertura) / apertura <= RANGO:
        indicadores = obtener_indicadores(activo, mercado)
        fila = {
            "Ticker": activo,
            "Mes": obtener_fecha_ultima_apertura(),
            "Apertura Mensual": round(apertura, 4),
            "Precio Actual": round(precio, 4),
            "Diferencia (%)": round((precio - apertura) / apertura * 100, 2),
            "RSI_4H": indicadores["RSI"]["4H"],
            "RSI_1D": indicadores["RSI"]["1D"],
            "RSI_1W": indicadores["RSI"]["1W"],
            "RSI_1M": indicadores["RSI"]["1M"],
            "Stoch_4H": indicadores["Stoch"]["4H"],
            "Stoch_1D": indicadores["Stoch"]["1D"],
            "Stoch_1W": indicadores["Stoch"]["1W"],
            "Stoch_1M": indicadores["Stoch"]["1M"]
        }
        filas.append(fila)

# 📌 DATAFRAME Y HTML
df = pd.DataFrame(filas)

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

html_tabla = generar_tabla_html(df)
titulo = f"Aperturas MO + Osciladores ({datetime.datetime.now().strftime('%Y-%m-%d')})"

# 📌 ACTUALIZACIÓN DEL POST
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
    print("✅ ¡Post actualizado con éxito!")
else:
    print(f"❌ Error al actualizar post: {response.status_code}, {response.text}")

# POST ANALISIS DE MERCADOS

import requests
import os
from bs4 import BeautifulSoup

# Configuración de WordPress
WORDPRESS_BASE_URL = "https://estrategiaelite.com/wp-json/wp/v2/posts/"
USERNAME = os.getenv("WORDPRESS_USER")
PASSWORD = os.getenv("WORDPRESS_PASSWORD")

# Configuración de Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Función para obtener contenido de los posts
def obtener_contenido_post(post_id):
    url = f"{WORDPRESS_BASE_URL}{post_id}"
    response = requests.get(url, auth=(USERNAME, PASSWORD))  # Autenticación aquí
    if response.status_code == 200:
        post_data = response.json()
        return post_data.get("content", {}).get("rendered", "")
    else:
        print(f"❌ Error al obtener el post {post_id}: {response.status_code}, {response.text}")
        return None

# IDs de los posts por categoría
POST_IDS = {
    "forex": [1151, 1225, 1198],
    "acciones_indices": [1028, 1032, 1015],
    "cripto": [1380, 1343, 1366]
}

# Extraer los posts de cada categoría
posts = {categoria: {post_id: obtener_contenido_post(post_id) for post_id in ids} for categoria, ids in POST_IDS.items()}

# Función para limpiar el HTML y extraer solo el contenido relevante
def limpiar_html(contenido_html):
    soup = BeautifulSoup(contenido_html, "html.parser")
    for tag in soup(["style", "script"]):
        tag.extract()
    return soup.get_text(separator="\n").strip()

# Función para extraer los activos de las tablas
def extraer_activos(contenido_html):
    soup = BeautifulSoup(contenido_html, "html.parser")
    activos = {"sobrecompra": [], "sobreventa": [], "mixtos": []}
    tablas = soup.find_all("table")
    
    if not tablas:
        print("❌ No se encontraron tablas en el post.")
        return activos

    for table in tablas:
        filas = table.find_all("tr")[1:]  # Ignorar la primera fila (encabezados)
        for fila in filas:
            columnas = fila.find_all("td")

            # Verificación antes de acceder a índices específicos
            if len(columnas) < 8:
                print(f"⚠ Tabla con solo {len(columnas)} columnas. Saltando fila.")
                continue  # Evitar errores en tablas con formato diferente

            ticker = columnas[0].text.strip()

            # Procesar valores dentro de <span> o texto normal
            def obtener_valor(columna):
                texto_limpio = columna.text.strip().replace(",", "").split()
                if not texto_limpio:  # ✅ Verificación extra
                    return 0.0  # Valor predeterminado si está vacío
                return float(texto_limpio[0])

            estocastico_4h = obtener_valor(columnas[4])
            estocastico_semanal = obtener_valor(columnas[6])
            estocastico_mensual = obtener_valor(columnas[7])

            # Clasificación según valores de osciladores
            if estocastico_semanal >= 80 or estocastico_mensual >= 80:
                activos["sobrecompra"].append(ticker)
            elif estocastico_semanal <= 20 or estocastico_mensual <= 20:
                activos["sobreventa"].append(ticker)
            else:
                activos["mixtos"].append(ticker)

    return activos

# Procesar los posts y organizar los activos por categoría
activos_finales = {categoria: {"sobrecompra": [], "sobreventa": [], "mixtos": []} for categoria in POST_IDS}

for categoria, posts_categoria in posts.items():
    for post_id, contenido in posts_categoria.items():
        print(f"\n🔎 Procesando post {post_id} ({categoria})...")
        activos_procesados = extraer_activos(contenido)
        for clave in activos_finales[categoria]:
            activos_finales[categoria][clave].extend(activos_procesados[clave])

# Eliminar duplicados
for categoria in activos_finales:
    for clave in activos_finales[categoria]:
        activos_finales[categoria][clave] = list(set(activos_finales[categoria][clave]))

# Generar informe en HTML organizado para WordPress
informe_html = f"""
<h2>📊 Análisis de Mercados </h2>

<h3>Forex</h3>
<h4>📌 En sobrecompra, cerca de posible reversión:</h4>
<ul>
    {''.join(f'<li>{activo}</li>' for activo in activos_finales["forex"]["sobrecompra"])}
</ul>

<h4>📌 En sobreventa, cerca de posible reversión:</h4>
<ul>
    {''.join(f'<li>{activo}</li>' for activo in activos_finales["forex"]["sobreventa"])}
</ul>

<h4>📌 En puntos clave con señales mixtas:</h4>
<ul>
    {''.join(f'<li>{activo}</li>' for activo in activos_finales["forex"]["mixtos"])}
</ul>

<h3>Índices y Acciones</h3>
<h4>📌 En sobrecompra, cerca de posible reversión:</h4>
<ul>
    {''.join(f'<li>{activo}</li>' for activo in activos_finales["acciones_indices"]["sobrecompra"])}
</ul>

<h4>📌 En sobreventa, cerca de posible reversión:</h4>
<ul>
    {''.join(f'<li>{activo}</li>' for activo in activos_finales["acciones_indices"]["sobreventa"])}
</ul>

<h4>📌 En puntos clave con señales mixtas:</h4>
<ul>
    {''.join(f'<li>{activo}</li>' for activo in activos_finales["acciones_indices"]["mixtos"])}
</ul>

<h3>Criptomonedas</h3>
<h4>📌 En sobrecompra, cerca de posible reversión:</h4>
<ul>
    {''.join(f'<li>{activo}</li>' for activo in activos_finales["cripto"]["sobrecompra"])}
</ul>

<h4>📌 En sobreventa, cerca de posible reversión:</h4>
<ul>
    {''.join(f'<li>{activo}</li>' for activo in activos_finales["cripto"]["sobreventa"])}
</ul>

<h4>📌 En puntos clave con señales mixtas:</h4>
<ul>
    {''.join(f'<li>{activo}</li>' for activo in activos_finales["cripto"]["mixtos"])}
</ul>
"""

# Publicar en WordPress
POST_ID = 2130
wordpress_url = f"{WORDPRESS_BASE_URL}{POST_ID}"
response = requests.put(wordpress_url, json={"content": informe_html}, auth=(USERNAME, PASSWORD))
print("✅ Informe publicado en WordPress" if response.status_code == 200 else f"❌ Error: {response.text}")

# Generar informe en Markdown para Telegram
informe_texto = f"""
📊 **Análisis de Mercados**  

### **Forex**  
📌 **En sobrecompra, cerca de posible reversión:**  
- {', '.join(activos_finales["forex"]["sobrecompra"])}

📌 **En sobreventa, cerca de posible reversión:**  
- {', '.join(activos_finales["forex"]["sobreventa"])}

📌 **En puntos clave con señales mixtas:**  
- {', '.join(activos_finales["forex"]["mixtos"])}

### **Índices y Acciones**  
📌 **En sobrecompra, cerca de posible reversión:**  
- {', '.join(activos_finales["acciones_indices"]["sobrecompra"])}

📌 **En sobreventa, cerca de posible reversión:**  
- {', '.join(activos_finales["acciones_indices"]["sobreventa"])}

📌 **En puntos clave con señales mixtas:**  
- {', '.join(activos_finales["acciones_indices"]["mixtos"])}

### **Criptomonedas**  
📌 **En sobrecompra, cerca de posible reversión:**  
- {', '.join(activos_finales["cripto"]["sobrecompra"])}

📌 **En sobreventa, cerca de posible reversión:**  
- {', '.join(activos_finales["cripto"]["sobreventa"])}

📌 **En puntos clave con señales mixtas:**  
- {', '.join(activos_finales["cripto"]["mixtos"])}
"""

# Enviar el informe a Telegram con Markdown
telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

telegram_data = {
    "chat_id": TELEGRAM_CHAT_ID,
    "text": informe_texto,
    "parse_mode": "Markdown"
}

response = requests.post(telegram_url, json=telegram_data)

if response.status_code == 200:
    print("✅ ¡Informe enviado exitosamente a Telegram con formato correcto!")
else:
    print(f"❌ Error al enviar a Telegram: {response.status_code}, {response.text}")

import requests
import os
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Configuración de WordPress y Telegram
WORDPRESS_BASE_URL = "https://estrategiaelite.com/wp-json/wp/v2/posts/"
USERNAME = os.getenv("WORDPRESS_USER")
PASSWORD = os.getenv("WORDPRESS_PASSWORD")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Función para obtener contenido de los posts
def obtener_contenido_post(post_id):
    url = f"{WORDPRESS_BASE_URL}{post_id}"
    response = requests.get(url, auth=(USERNAME, PASSWORD))
    if response.status_code == 200:
        post_data = response.json()
        return post_data.get("content", {}).get("rendered", "")
    else:
        print(f"❌ Error al obtener el post {post_id}: {response.status_code}, {response.text}")
        return None

# Función para extraer y filtrar eventos por fecha
def filtrar_eventos(contenido_html, dias_rango, tipo_evento):
    soup = BeautifulSoup(contenido_html, "html.parser")
    eventos_futuros = []

    # Obtener la fecha actual
    fecha_actual = datetime.now()
    fecha_limite = fecha_actual + timedelta(days=dias_rango)

    # Buscar todas las filas de las tablas
    for table in soup.find_all("table"):
        filas = table.find_all("tr")[1:]  # Ignorar encabezados
        for fila in filas:
            columnas = fila.find_all("td")
            if len(columnas) < 2:
                continue

            nombre_evento = columnas[0].text.strip()
            fecha_evento = columnas[1].text.strip()

            # Convertir la fecha en formato de datetime
            try:
                fecha_dt = datetime.strptime(fecha_evento, "%b %d, %Y")
                if fecha_actual <= fecha_dt <= fecha_limite:
                    eventos_futuros.append(f"- {nombre_evento} → {fecha_evento}")
            except ValueError:
                print(f"⚠ Error con formato de fecha en evento: {nombre_evento}, intentando otra conversión...")

                # Detectar si la fecha tiene otro formato (Ejemplo: "Jun 18, 18:00")
                try:
                    fecha_dt = datetime.strptime(fecha_evento, "%b %d, %H:%M")
                    fecha_dt = fecha_dt.replace(year=fecha_actual.year)  # Asignar el año actual si falta
                    if fecha_actual <= fecha_dt <= fecha_limite:
                        eventos_futuros.append(f"- {nombre_evento} → {fecha_dt.strftime('%b %d, %Y %H:%M')}")
                except ValueError:
                    print(f"⚠ No se pudo convertir la fecha de {nombre_evento}, formato desconocido.")

    return eventos_futuros

# Obtener eventos económicos en los próximos 7 días
post_id_economicos = 1045
contenido_economicos = obtener_contenido_post(post_id_economicos)
eventos_economicos = filtrar_eventos(contenido_economicos, 7, "Indicadores Económicos")

# Obtener reportes de ganancias en los próximos 15 días
post_id_ganancias = 1050  # Reemplaza con el ID correcto del post de reportes de ganancias
contenido_ganancias = obtener_contenido_post(post_id_ganancias)
eventos_ganancias = filtrar_eventos(contenido_ganancias, 15, "Reportes de Ganancias")

# Generar mensaje para Telegram
mensaje_telegram = "📊 **Próximos eventos económicos y reportes de ganancias**\n\n"

if eventos_economicos:
    mensaje_telegram += "📌 **Indicadores Económicos (Próximos 7 días)**:\n" + "\n".join(eventos_economicos) + "\n\n"
if eventos_ganancias:
    mensaje_telegram += "📌 **Reportes de Ganancias (Próximos 15 días)**:\n" + "\n".join(eventos_ganancias) + "\n\n"

# Solo enviar si hay eventos
if eventos_economicos or eventos_ganancias:
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    response = requests.post(telegram_url, json={"chat_id": TELEGRAM_CHAT_ID, "text": mensaje_telegram, "parse_mode": "Markdown"})

    if response.status_code == 200:
        print("✅ ¡Informe enviado exitosamente a Telegram!")
    else:
        print(f"❌ Error al enviar a Telegram: {response.status_code}, {response.text}")
else:
    print("🚫 No hay eventos próximos, no se envió mensaje a Telegram.")


