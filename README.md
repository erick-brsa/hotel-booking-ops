# Proyecto: Calidad de Datos para Reservaciones Hoteleras

## 1. Descripción

Este proyecto aborda la fragmentación y mala calidad de los datos de reservaciones en **Sunset Hospitality Group**, una cadena hotelera que opera un hotel urbano (City Hotel) y un hotel vacacional (Resort Hotel). La cadena recibe reservas a través de dos fuentes: su sistema interno y canales externos (Booking, Expedia, agencias de viaje).

El objetivo es consolidar ambas fuentes en un solo dataset confiable bajo un modelo canónico, aplicando técnicas de limpieza, estandarización y Record Linkage para eliminar duplicados y mejorar la calidad de los datos.

## 2. Problemática

- **Problema detectado**: Las dos fuentes de datos describen las mismas reservas pero utilizan formatos distintos (nombres de columnas en español vs inglés, fechas inconsistentes). Además, la fuente externa presenta valores faltantes, nombres mal escritos y duplicidad potencial de clientes.

- **Objetivo**: Consolidar los registros de reservaciones provenientes de múltiples canales en una sola base de datos confiable que permita el análisis y la toma de decisiones estratégicas.

## 3. Estructura del Repositorio

```text
hotel_booking_project/
├── data/
│   ├── raw/
│   │   ├── internal_bookings.csv
│   │   └── external_bookings.csv
│   ├── processed/
│   │   ├── internal_clean.csv
│   │   ├── external_clean.csv
│   │   ├── unified_dataset.csv
│   │   └── consolidated_bookings.csv
│   └── results/
│       ├── dqs_comparison.csv
│       ├── initial_metrics.json
│       └── model_results.csv
├── notebooks/
│   ├── 01_perfilado_inicial.ipynb
│   ├── 02_limpieza_estandarizacion.ipynb
│   ├── 03_integracion_estandarizacion.ipynb
│   ├── 04_perfilado_integracion.ipynb
│   ├── 05_record_linkage.ipynb
│   ├── 06_analisis_modelos.ipynb
│   └── 07_dqs_final.ipynb
├── tools/
│   └── corruptor.py
├── pyproject.toml
└── README.md
```

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

## 5. Ejecución del Pipeline

El pipeline se ejecuta secuencialmente siguiendo los notebooks en orden:

1. **`01_perfilado_inicial.ipynb`**  
   Perfilado individual de cada fuente original (sistema interno y canales externos). Se generan reportes automáticos con `sweetviz` y se calculan las métricas iniciales del índice de calidad (DQS).

2. **`02_limpieza_estandarizacion.ipynb`**  
   Limpieza individual de cada fuente: renombrado de columnas (español → inglés), unificación de formatos de fecha, homologación de estatus, imputación de nulos con KNN (numéricas) y moda (categóricas), y validación de rangos numéricos. Los datos limpios se guardan por separado.

3. **`03_integracion.ipynb`**  
   Unión vertical de ambas fuentes ya limpias en un solo dataset (`unified_dataset.csv`).

4. **`04_perfilado_integrado.ipynb`**  
   Perfilado del dataset unificado para identificar duplicados entre fuentes y medir el estado previo al Record Linkage.

5. **`05_record_linkage.ipynb`**  
   Identificación y fusión de clientes duplicados entre fuentes mediante comparación difusa (distancia de Levenshtein) y bloqueo por email. Se genera el dataset consolidado final.

6. **`06_analisis_modelos.ipynb`**  
   Entrenamiento de modelos para responder las preguntas de negocio: Random Forest (factores de cancelación y clasificación alto/bajo valor) y K-Means (perfiles de huéspedes recurrentes).

7. **`07_dqs_final.ipynb`**  
   Cálculo del índice de calidad final (DQS) sobre el dataset consolidado, comparación con las métricas iniciales y visualización de la mejora.

## 6. Metodología

Se adoptó de forma ligera el marco **Total Data Quality Management (TDQM)** con cuatro fases:

- **Definir**: Se establecieron dimensiones de calidad: Completitud, Consistencia, Unicidad y Validez.
- **Medir**: Se definieron métricas cuantitativas para cada dimensión.
- **Analizar**: Se realizó un perfilado exhaustivo de ambas fuentes.
- **Mejorar**: Se implementó un pipeline de limpieza, estandarización, Record Linkage e imputación.

El impacto se cuantificó mediante un **índice de calidad (DQS)** aplicado antes y después del proceso.

## 7. Tecnologías y Herramientas

- Python 
- Pandas / NumPy
- missingno (visualización de nulos)
- sweetviz (reportes automáticos)
- recordlinkage (comparación difusa y consolidación)
- scikit-learn (KNNImputer, Random Forest, K-Means)
- plotly (visualizaciones interactivas)
- Jupyter Notebooks
- UV (Python package and environment manager)
- Draw.io (diagrama de integración)
