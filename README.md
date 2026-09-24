# Monitor Analítico de Riesgo Crediticio y Morosidad

Proyecto Power BI en formato `.pbip` para analizar una cartera de créditos, medir la morosidad y apoyar decisiones de originación, seguimiento y segmentación de riesgo.

## Resumen Ejecutivo

El tablero consolida información individual de créditos y solicitantes para responder cuatro preguntas de negocio:

1. ¿Cuál es el volumen total de créditos y el monto desembolsado?
2. ¿Qué proporción de la cartera está en default?
3. ¿Cómo se comportan el ingreso, el DTI y la tasa de interés por segmento?
4. ¿Qué grupos requieren políticas diferenciadas de aprobación, monitoreo o cobranza?

La versión validada del modelo contiene **32.581 créditos** y un monto total desembolsado de **312.431.300** unidades monetarias, calculado directamente desde la tabla de créditos. Los valores monetarios deben interpretarse según la moneda definida por la fuente de datos.

## Objetivo de Negocio

El objetivo es proporcionar una vista ejecutiva y reproducible de la exposición crediticia de la cartera. El modelo permite segmentar clientes por nivel de riesgo, ingresos, intención del préstamo, propiedad de vivienda y características del crédito, con foco en:

- Detectar concentración de defaults.
- Comparar morosidad entre segmentos de clientes y productos.
- Relacionar capacidad de pago, ingresos y monto solicitado mediante DTI.
- Identificar grupos de ingresos para orientar límites, precios y estrategias de cobranza.
- Mantener las métricas principales centralizadas en una tabla de medidas.

## Arquitectura del Proyecto

El repositorio utiliza Power BI Project en modo desarrollo. El archivo `.pbip` referencia por separado la definición del reporte y la del modelo semántico, lo que facilita el control de cambios con Git.

```text
.
├── data/
│   ├── raw/                                      # Datos originales o descargados
│   └── processed/
│       └── creditos_latam_limpio.csv              # Fuente consumida por Power Query
├── mcp_server/
│   └── server.py                                  # Servidor auxiliar del proyecto
├── power_bi/
│   ├── dashboard_riesgo_credito.pbip              # Punto de entrada del proyecto
│   ├── dashboard_riesgo_credito.Report/           # Páginas, tema y configuración visual
│   └── dashboard_riesgo_credito.SemanticModel/   # Modelo, tablas, columnas y medidas TMDL
├── scripts/
│   └── etl_credit_risk.py                         # Descarga, limpieza y enriquecimiento del dataset
├── .gitignore
└── README.md
```

## Modelo de Datos

El modelo semántico tiene cultura `es-CO`, nivel de compatibilidad 1606 y dos tablas:

### `creditos_latam_limpio`

Es la tabla principal de hechos, en modo **Import**, cargada desde `data/processed/creditos_latam_limpio.csv` mediante Power Query. Cada fila representa un crédito y `ID_Credito` identifica el registro.

| Grupo | Columnas | Uso de negocio |
|---|---|---|
| Identificación | `ID_Credito` | Conteo de créditos y trazabilidad del registro |
| Perfil del solicitante | `person_age`, `person_income`, `person_home_ownership`, `person_emp_length` | Segmentación demográfica y capacidad económica |
| Crédito | `loan_amnt`, `loan_int_rate`, `loan_status`, `loan_percent_income` | Exposición, precio, estado y carga relativa del préstamo |
| Características | `loan_intent`, `loan_grade` | Finalidad y clasificación del crédito |
| Historial | `cb_person_default_on_file`, `cb_person_cred_hist_length` | Antecedentes y antigüedad del historial crediticio |
| Indicadores derivados | `Ratio_DTI`, `Indicador_Default`, `Nivel_Riesgo` | DTI, bandera de default y nivel de riesgo |
| Segmentación calculada | `Rango_Salarial` | Tramos de ingreso para análisis ejecutivo |

`Rango_Salarial` se calcula con los siguientes tramos:

- `1. Bajo (< $20k)`
- `2. Medio-Bajo ($20k - $35k)`
- `3. Medio-Alto ($35k - $55k)`
- `4. Alto ($55k - $85k)`
- `5. Muy Alto (> $85k)`
- `Sin Información` para ingresos nulos

### `_Medidas_Riesgo`

Tabla calculada contenedora de medidas. Incluye una columna técnica oculta (`TablaMedidas`) y concentra los indicadores reutilizables del reporte:

| Medida | Cálculo | Formato |
|---|---|---|
| `Monto Total Desembolsado` | Suma de `loan_amnt` | Moneda |
| `Total Creditos` | Conteo no vacío de `ID_Credito` | Número entero |
| `Creditos en Default` | Suma de `Indicador_Default` | Número entero |
| `Tasa de Default %` | `Creditos en Default / Total Creditos` | `0.00%` |
| `Ratio DTI Promedio %` | Promedio de `Ratio_DTI / 10000` | `0.00%` |
| `Tasa Interes Promedio %` | Promedio de `loan_int_rate / 10000` | `0.00%` |

Las divisiones por `10000` reflejan la escala actualmente observada en el modelo importado y convierten los promedios a valores decimales antes de aplicar el formato porcentual. Si cambia la escala de la fuente, estas medidas deben revisarse junto con el ETL.

## Flujo ETL

[`scripts/etl_credit_risk.py`](scripts/etl_credit_risk.py) realiza estas tareas:

1. Descarga el dataset de riesgo crediticio desde Kaggle mediante `kagglehub`.
2. Imputa valores nulos en `person_emp_length` y `loan_int_rate` usando la mediana.
3. Calcula `Ratio_DTI` como `loan_amnt / person_income` cuando el ingreso es positivo.
4. Genera `Indicador_Default` a partir de `loan_status`.
5. Clasifica `Nivel_Riesgo` según `loan_int_rate`.
6. Genera `ID_Credito` y escribe el CSV procesado.

Power BI consume el CSV procesado desde una ruta local configurada en la partición TMDL. Para mover el proyecto a otra máquina, se debe actualizar esa ruta o parametrizarla en Power Query.

## Reporte Power BI

El reporte contiene una página (`Página 1`) configurada en formato `FitToPage`, con lienzo de 1920 × 1150. Usa el tema base `Fluent2-CY26SU08` y un tema personalizado registrado en los recursos del reporte. La definición visual se encuentra en `dashboard_riesgo_credito.Report/definition/`.

## Requisitos y Uso

- Power BI Desktop con soporte para proyectos `.pbip`.
- Python para ejecutar el ETL.
- Dependencias Python: `kagglehub`, `numpy` y `pandas`.
- Credenciales/configuración necesarias para descargar el dataset desde Kaggle.

Para regenerar el archivo procesado:

```powershell
python scripts/etl_credit_risk.py
```

Después, abrir `power_bi/dashboard_riesgo_credito.pbip` en Power BI Desktop y actualizar el modelo.

## Control de Versiones

Se excluyen archivos temporales y cachés locales de Power BI mediante `.gitignore`. Las definiciones TMDL, el reporte, el ETL y la documentación permanecen versionables para facilitar auditoría y revisión de cambios.