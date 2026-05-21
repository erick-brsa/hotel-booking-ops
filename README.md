# Proyecto: Calidad de Datos para Reservaciones Hoteleras

## 1. Descripción

Este proyecto implementa un pipeline integral de Calidad de Datos (*Data Quality*) aplicado a un dataset de reservaciones hoteleras. A través de procesos de perfilado, limpieza, integración y análisis, se transforman datos heterogéneos en un Dataset Maestro confiable para la toma de decisiones.

---

## 2. Problemática

- **Problema detectado**: Existen inconsistencias en la estructura de los datos, como diferencias en nombres de hoteles, formatos de fecha y valores faltantes, lo que dificulta un análisis coherente.
- **Objetivo**: Implementar un pipeline de preprocesamiento capaz de resolver inconsistencias, eliminar duplicados mediante *record linkage* y estandarizar la información bajo un modelo canónico.

---

## 3. Estructura del Repositorio

```text
hotel_booking_project/
├── data/
│   ├── raw/
│   ├── processed/
│   └── master/
├── notebooks/
│   ├── 01_profiling.ipynb
│   ├── 02_cleaning.ipynb
│   ├── 03_fusion.ipynb
│   └── 04_analysis.ipynb
├── src/
│   ├── profiling.py
│   ├── cleaning.py
│   ├── fusion.py
│   └── analysis.py
├── pyproject.toml
└── README.md
```

---

## 4. Configuración del Entorno (Instalación de UV)

Este proyecto utiliza `uv` para la gestión de dependencias y entornos virtuales.

### 4.1 Instalar uv

#### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### macOS / Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 4.2 Sincronizar Dependencias

Una vez instalado `uv`, navega a la raíz del proyecto y ejecuta:

```bash
uv sync
```

---

## 5. Ejecución del Pipeline (Orden Secuencial)

Para garantizar integridad, reproducibilidad y trazabilidad, los scripts deben ejecutarse en el siguiente orden.

### 5.1 Profiling

Identifica anomalías, inconsistencias e indicadores iniciales de calidad de datos.

```bash
uv run src/profiling.py
```

### 5.2 Cleaning

Aplica transformaciones y correcciones con base en el diagnóstico realizado.

```bash
uv run src/cleaning.py
```

### 5.3 Fusion

Integra las fuentes limpias en un modelo canónico unificado.

```bash
uv run src/fusion.py
```

### 5.4 Analysis

Extrae conocimiento e insights del dataset consolidado.

```bash
uv run src/analysis.py
```

---

## 6. Metodología

El proyecto sigue un flujo estructurado de Calidad de Datos compuesto por las siguientes fases:

1. Profiling  
2. Cleaning  
3. Integration  
4. Analysis

---

## 7. Tecnologías y Herramientas

- Python
- Pandas
- NumPy
- UV (*Python package and environment manager*)

---
