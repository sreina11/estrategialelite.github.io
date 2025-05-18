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

# ⚠️ Instalar librerías necesarias
import requests
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
    "XAUUSD": "OANDA",  # ✅ Oro con exchange correcto
    "DXY": "TVC"        # ✅ Índice del dólar (US Dollar Index)
}

# **Temporalidades**
temporalidades = {
    "4H": Interval.INTERVAL_4_HOURS,
    "Diario": Interval.INTERVAL_1_DAY,
    "Semanal": Interval.INTERVAL_1_WEEK,
    "Mensual": Interval.INTERVAL_1_MONTH
}

# **Diccionario para almacenar los datos**
data = []
filtered_data = []

# **Obtener datos desde TradingView**
for activo, mercado in activos.items():
    fila = {"Ticker": activo}

    for periodo_nombre, intervalo in temporalidades.items():
        try:
            handler = TA_Handler(symbol=activo, exchange=mercado, screener="forex" if mercado == "FX" else "cfd", interval=intervalo)
            analysis = handler.get_analysis()

            precio = analysis.indicators.get("close", None)
            bb_upper = analysis.indicators.get("BB.upper", None)
            bb_lower = analysis.indicators.get("BB.lower", None)
            rsi = analysis.indicators.get("RSI", None)
            stoch = analysis.indicators.get("Stoch.K", None)

            fila[f"Precio_{periodo_nombre}"] = precio
            fila[f"BB_Upper_{periodo_nombre}"] = bb_upper
            fila[f"BB_Lower_{periodo_nombre}"] = bb_lower
            fila[f"RSI_{periodo_nombre}"] = rsi
            fila[f"Stoch_{periodo_nombre}"] = stoch

            # **Filtrar activos con confluencias**
            if precio and bb_upper and bb_lower and (rsi is not None) and (stoch is not None):
                if (precio >= bb_upper or precio <= bb_lower) and (rsi >= 70 or rsi <= 30 or stoch >= 80 or stoch <= 20):
                    filtered_data.append(fila)

        except Exception as e:
            print(f"Error obteniendo datos para {activo} ({periodo_nombre}): {e}")

    data.append(fila)

# **Crear DataFrame**
df_confluencias = pd.DataFrame(filtered_data)

# **Mostrar activos con confluencias en Bandas de Bollinger, RSI y Estocástico**
print("\n📊 Activos con confluencias (fuera de Bandas de Bollinger y RSI/Stoch en sobrecompra o sobreventa):")
print(df_confluencias if not df_confluencias.empty else "No hay activos con confluencias.")

# POST CONFLUENCIAS BANDAS DE BOLLINER RSI ESTOC

# ⚠️ Instalar librerías necesarias
import requests
import pandas as pd
import datetime
import os  # Para manejar credenciales de WordPress desde secretos

# **Post ID del post ya creado**
post_id = "1151"

# **URL de la API para actualizar el post**
wordpress_url = f"https://estrategiaelite.com/wp-json/wp/v2/posts/{post_id}"

# **Función para aplicar colores a los indicadores**
def aplicar_colores(valor, indicador):
    """Aplica colores y negrita basados en el valor de RSI o Stoch.K."""
    if pd.notna(valor):  # Evita errores con valores nulos
        if indicador == "RSI":
            if valor >= 70:
                return f'<span style="color: red; font-weight: bold;">{valor}</span>'  # RSI sobrecompra
            elif valor <= 30:
                return f'<span style="color: green; font-weight: bold;">{valor}</span>'  # RSI sobreventa
        elif indicador == "Stoch":
            if valor >= 80:
                return f'<span style="color: red; font-weight: bold;">{valor}</span>'  # Estocástico sobrecompra
            elif valor <= 20:
                return f'<span style="color: green; font-weight: bold;">{valor}</span>'  # Estocástico sobreventa
    return f'<span style="font-weight: bold;">{valor}</span>'  # Negrita sin color

# ✅ **Tomar el DataFrame original (`df_confluencias`) sin modificaciones**
df_coloreado = df_confluencias.copy()

# **Aplicar colores a RSI y Estocástico**
for col in df_confluencias.columns:
    if "RSI" in col:
        df_coloreado[col] = df_coloreado[col].apply(lambda x: aplicar_colores(x, "RSI"))
    elif "Stoch" in col:
        df_coloreado[col] = df_coloreado[col].apply(lambda x: aplicar_colores(x, "Stoch"))

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
    "title": f"Confluencias de Bandas de Bollinger, RSI y Estocástico - Actualización {datetime.datetime.now().strftime('%Y-%m-%d')}",
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
    print("✅ ¡Publicación de confluencias actualizada exitosamente en WordPress!")
else:
    print(f"❌ Error al actualizar en WordPress: {response.status_code}, {response.text}")
