"""
Script para generar `fuente_2_agencia.csv` a partir de `internal_bookings.csv`.
Simula la base de datos de una agencia de viajes externa con:
  - Modelo canónico (renombrado de columnas)
  - Ruido e inconsistencias para practicar limpieza de datos
  - Preparación para record-linkage con la fuente original
"""

import pandas as pd
import numpy as np
import random
from pathlib import Path

# ──────────────────────────────────────────────
# 1. CARGA Y PREPARACIÓN
# ──────────────────────────────────────────────

# Semilla para reproducibilidad
random.seed(42)
np.random.seed(42)

# Definición de rutas
BASE_DIR = Path(__file__).resolve().parent.parent
# APUNTA AL EXISTENTE:
INPUT_PATH = BASE_DIR / "data" / "raw" / "internal_bookings.csv"
# APUNTA AL QUE SE VA A CREAR:
OUTPUT_PATH = BASE_DIR / "data" / "raw" / "external_bookings.csv"

# Lee el archivo fuente
df_original = pd.read_csv(INPUT_PATH)

# Crea una copia para no alterar el DataFrame original
df = df_original.sample(frac=1, random_state=42).reset_index(drop=True)

print(f"[OK] Dataset cargado: {df.shape[0]} filas × {df.shape[1]} columnas")


# ─────────────────────────────────────────────────
# 2. TRANSFORMACIÓN DE ESTRUCTURA (MODELO CANÓNICO)
# ─────────────────────────────────────────────────

# Renombra 8+ columnas clave para simular un sistema externo distinto
rename_map = {
    "hotel":                        "tipo_alojamiento",
    "name":                         "nombre_huesped",
    "email":                        "correo_electronico",
    "phone-number":                 "telefono_contacto",
    "country":                      "pais_origen",
    "customer_type":                "categoria_cliente",
    "adr":                          "tarifa_diaria_promedio",
    "market_segment":               "segmento_mercado",
    "deposit_type":                 "tipo_deposito",
    "reservation_status":           "estado_reserva",
    "reservation_status_date":      "fecha_estado_reserva",
    "lead_time":                    "dias_anticipacion",
    "total_of_special_requests":    "total_solicitudes_especiales",
}
df.rename(columns=rename_map, inplace=True)

print(f"[OK] Columnas renombradas: {list(rename_map.values())}")


# ──────────────────────────────────────────────
# 3. INYECCIÓN DE RUIDO Y ANOMALÍAS
# ──────────────────────────────────────────────

# — 3a. VALORES NULOS (5 % aleatorio en columnas seleccionadas) ——————————

# Columnas de texto y numéricas sobre las que se introducen nulos
# Se excluye 'is_canceled' (protegida) y columnas de fecha (se tratarán aparte)
columnas_con_ruido = [
    "tipo_alojamiento",
    "correo_electronico",
    "telefono_contacto",
    "pais_origen",
    "categoria_cliente",
    "segmento_mercado",
    "tipo_deposito",
    "estado_reserva",
    "tarifa_diaria_promedio",
    "dias_anticipacion",
    "solicitudes_especiales",
    "stays_in_weekend_nights",
    "stays_in_week_nights",
    "adults",
    "children",
    "meal",
    "assigned_room_type",
]

for col in columnas_con_ruido:
    if col not in df.columns:
        continue
    mask = np.random.rand(len(df)) < 0.05
    # Aplicamos los nulos donde la máscara sea True
    df.loc[mask, col] = np.nan

print(f"[OK] Valores nulos introducidos (~5 %) en {len(columnas_con_ruido)} columnas")


# — 3b. INCONSISTENCIAS EN NOMBRES (para de-duplicación) ———————————————

def alterar_nombre(nombre):
    """Aplica una de tres alteraciones al azar sobre un nombre de huésped."""
    if pd.isna(nombre):
        return nombre

    nombre_str = str(nombre)
    opcion = random.randint(1, 3)

    if opcion == 1:
        return str(nombre).upper()           # TODAS MAYÚSCULAS

    elif opcion == 2:
        return str(nombre).lower()           # todas minúsculas

    else:
        letras_indices = [i for i, char in enumerate(nombre_str) if char != ' ']
        
        if len(letras_indices) > 1:
            pos = random.choice(letras_indices)
            # Elimina solo la letra en esa posición, dejando el espacio intacto
            return nombre_str[:pos] + nombre_str[pos+1:]
        
        return nombre_str


# Aplica la alteración al 70 % de las filas (el 30 % queda con el nombre original)
mascara_alterar = np.random.rand(len(df)) < 0.70
df.loc[mascara_alterar, "nombre_huesped"] = (
    df.loc[mascara_alterar, "nombre_huesped"].apply(alterar_nombre)
)

print("[OK] Nombres alterados en ~70 % de las filas (mayúsculas / minúsculas / truncado)")


# — 3c. FORMATO INCONSISTENTE DE FECHAS ————————————————————————————————

# Mapeo de nombres de mes en inglés (tal como vienen en el CSV) a número
MES_A_NUM = {
    "January": "01", "February": "02", "March": "03", "April": "04",
    "May": "05", "June": "06", "July": "07", "August": "08",
    "September": "09", "October": "10", "November": "11", "December": "12"
}

def construir_fecha_inconsistente(row):
    """
    Combina año, mes y día en dos formatos alternos según el índice de la fila:
      - Filas pares  → YYYY/MM/DD
      - Filas impares → DD-MM-YYYY
    """
    try:
        anio = str(int(row["arrival_date_year"]))
        mes  = MES_A_NUM.get(str(row["arrival_date_month"]), "00")
        dia  = str(int(row["arrival_date_day_of_month"])).zfill(2)
    except (ValueError, KeyError):
        return np.nan

    if row.name % 2 == 0:            # Fila par → formato ISO con barra
        return f"{anio}/{mes}/{dia}"
    else:                             # Fila impar → formato europeo con guión
        return f"{dia}-{mes}-{anio}"


# Crea la nueva columna con fechas inconsistentes
df["fecha_llegada"] = df.apply(construir_fecha_inconsistente, axis=1)

# Elimina las columnas originales de año, mes y día (ya consolidadas)
df.drop(columns=[
    "arrival_date_year",
    "arrival_date_month",
    "arrival_date_day_of_month",
    "arrival_date_week_number",   # también la semana, no aporta al linkage
], inplace=True)

print("[OK] Fechas de llegada combinadas con formato YYYY/MM/DD y DD-MM-YYYY alternos")


# ──────────────────────────────────────────────
# 4. PRESERVACIÓN ANALÍTICA
# ──────────────────────────────────────────────

# Verifica que 'is_canceled' no tiene nulos (ni fue renombrada)
assert "is_canceled" in df.columns, "ERROR: falta la columna is_canceled"
assert df["is_canceled"].isna().sum() == 0, "ERROR: is_canceled tiene valores nulos"

print(f"[OK] 'is_canceled' intacta: {df['is_canceled'].value_counts().to_dict()}")


# ──────────────────────────────────────────────
# 5. EXPORTACIÓN
# ──────────────────────────────────────────────

# Guarda el resultado sin incluir el índice de pandas
df.to_csv(OUTPUT_PATH, index=False)

print(f"\n[LISTO] Archivo exportado → {OUTPUT_PATH}")
print(f"        Dimensiones finales: {df.shape[0]} filas × {df.shape[1]} columnas")
print(f"        Columnas: {df.columns.tolist()}")
