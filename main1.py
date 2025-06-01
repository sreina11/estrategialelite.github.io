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

# CONFLUENCIAS MEDIAS MOVILES Y OSCILADORES 
import requests
import os
import datetime
import pandas as pd
from tradingview_ta import TA_Handler, Interval

# 📌 Datos de WordPress
post_id = "1198"
wordpress_url = f"https://estrategiaelite.com/wp-json/wp/v2/posts/{post_id}"

def aplicar_formato(valor, decimales):
    return round(valor, decimales) if valor is not None else None

# 📊 Activos y Exchanges
activos = {
    "USDJPY": "FX", "USDCAD": "FX", "USDCHF": "FX", "GBPUSD": "FX",
    "GBPJPY": "FX", "EURAUD": "FX", "EURUSD": "FX", "EURJPY": "FX",
    "EURGBP": "FX", "AUDUSD": "FX", "AUDJPY": "FX", "NZDUSD": "FX",
    "CHFJPY": "FX", "CADJPY": "FX", "CADCHF": "FX", "XAUUSD": "OANDA",
    "DXY": "TVC"
}

# 🕒 Intervalos
intervalos_ma = {
    "Semanal": Interval.INTERVAL_1_WEEK,
    "Mensual": Interval.INTERVAL_1_MONTH
}
intervalos_osciladores = {
    "RSI_4H": Interval.INTERVAL_4_HOURS, "RSI_1D": Interval.INTERVAL_1_DAY,
    "RSI_1W": Interval.INTERVAL_1_WEEK, "RSI_1M": Interval.INTERVAL_1_MONTH,
    "Stoch_4H": Interval.INTERVAL_4_HOURS, "Stoch_1D": Interval.INTERVAL_1_DAY,
    "Stoch_1W": Interval.INTERVAL_1_WEEK, "Stoch_1M": Interval.INTERVAL_1_MONTH
}

# 📊 Obtener datos de TradingView
confluencias = []

for activo, exchange in activos.items():
    fila = {"Ticker": activo}
    try:
        # Obtener osciladores
        for nombre, intervalo in intervalos_osciladores.items():
            handler = TA_Handler(symbol=activo, exchange=exchange,
                                 screener="forex" if exchange == "FX" else "cfd",
                                 interval=intervalo)
            analisis = handler.get_analysis()
            if "RSI" in nombre:
                fila[nombre] = aplicar_formato(analisis.indicators.get("RSI"), 2)
            elif "Stoch" in nombre:
                fila[nombre] = aplicar_formato(analisis.indicators.get("Stoch.K"), 2)

        # Obtener precios y medias móviles
        for periodo, intervalo in intervalos_ma.items():
            handler = TA_Handler(symbol=activo, exchange=exchange,
                                 screener="forex" if exchange == "FX" else "cfd",
                                 interval=intervalo)
            analisis = handler.get_analysis()

            precio = aplicar_formato(analisis.indicators.get("close"), 4)
            ma200 = aplicar_formato(analisis.indicators.get("SMA200"), 4)
            ma50 = aplicar_formato(analisis.indicators.get("SMA50"), 4)
            ma20 = aplicar_formato(analisis.indicators.get("SMA20"), 4)

            if precio:
                fila["Precio"] = precio
                for ma, nombre_ma in [(ma200, "MA200"), (ma50, "MA50"), (ma20, "MA20")]:
                    fila[f"{nombre_ma}_{periodo}"] = ma
                    if ma:
                        rango = aplicar_formato(((precio - ma) / ma) * 100, 1)
                        fila[f"Rango_{nombre_ma}_{periodo}"] = rango

    except Exception as e:
        print(f"⚠️ Error con {activo}: {e}")
        continue

    confluencias.append(fila)

# Crear DataFrame
df = pd.DataFrame(confluencias)

# 🎯 Filtrar confluencias técnicas
# Precio dentro de ±0.5% de alguna MA (semanal o mensual)
cond_ma = df[[col for col in df.columns if col.startswith("Rango_")]].apply(
    lambda row: any(-0.5 <= val <= 0.5 for val in row if pd.notnull(val)), axis=1
)

# RSI extremos
cond_rsi = df[[col for col in df.columns if col.startswith("RSI")]].apply(
    lambda row: any((val <= 30 or val >= 70) for val in row if pd.notnull(val)), axis=1
)

# Stoch extremos
cond_stoch = df[[col for col in df.columns if col.startswith("Stoch")]].apply(
    lambda row: any((val <= 20 or val >= 80) for val in row if pd.notnull(val)), axis=1
)

# Filtrar activos que cumplan confluencias
df_filtrado = df[(cond_ma) & (cond_rsi | cond_stoch)].copy()

# 🧱 Generar HTML organizado
def generar_tabla_html(df):
    estructura = "<h2>Confluencias MA + Osciladores</h2>"

    for ma_tipo in ["MA200", "MA50", "MA20"]:
        for periodo in ["Semanal", "Mensual"]:
            for oscilador in ["RSI", "Stoch"]:
                titulo = f"<h3>{ma_tipo} {periodo} ±0.5% + {oscilador}</h3>"
                columnas = ["Ticker", "Precio", f"{ma_tipo}_{periodo}", f"Rango_{ma_tipo}_{periodo}"]

                if oscilador == "RSI":
                    columnas += [c for c in df.columns if c.startswith("RSI")]
                elif oscilador == "Stoch":
                    columnas += [c for c in df.columns if c.startswith("Stoch")]

                # Filtrar filas con valores válidos para ese MA y oscilador
                subset_df = df[(df[f"Rango_{ma_tipo}_{periodo}"].between(-0.5, 0.5)) & 
                               df[columnas].notnull().all(axis=1)].copy()

                # Filtrar por oscilador extremo
                if oscilador == "RSI":
                    subset_df = subset_df[
                        subset_df[[c for c in df.columns if c.startswith("RSI")]].apply(
                            lambda row: any((val <= 30 or val >= 70) for val in row if pd.notnull(val)), axis=1)
                    ]
                else:
                    subset_df = subset_df[
                        subset_df[[c for c in df.columns if c.startswith("Stoch")]].apply(
                            lambda row: any((val <= 20 or val >= 80) for val in row if pd.notnull(val)), axis=1)
                    ]

                if subset_df.empty:
                    estructura += titulo + "<p>No hay confluencias</p>"
                else:
                    estructura += titulo + subset_df[columnas].to_html(index=False, escape=False)

    return estructura

# 📝 Publicar en WordPress
post_data = {
    "title": f"Confluencias MA + Osciladores - Actualización {datetime.datetime.now().strftime('%Y-%m-%d')}",
    "content": generar_tabla_html(df_filtrado)
}

response = requests.put(
    wordpress_url,
    json=post_data,
    auth=(os.getenv("WORDPRESS_USER"), os.getenv("WORDPRESS_PASSWORD"))
)

# ✅ Resultado
if response.status_code == 200:
    print("✅ ¡Publicación de confluencias actualizada exitosamente en WordPress!")
else:
    print(f"❌ Error al actualizar confluencias: {response.status_code}, {response.text}")

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


