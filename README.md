# 📊 Monitor Analítico de Riesgo Crediticio y Morosidad - FinTech LATAM

![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![DAX](https://img.shields.io/badge/DAX-0078D4?style=for-the-badge&logo=microsoft&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)

## 🎯 Objetivo del Proyecto
Diseño e implementación de un dashboard ejecutivo interactivo en Power BI para la evaluación de exposición, tasa de impago (Default), DTI (Debt-to-Income) y segmentación socioeconómica sobre una cartera de crédito FinTech compuesta por **$312.4M USD** repartidos en **32,581 créditos**.

---

## 🛠️ Stack Tecnológico y Arquitectura
* **Business Intelligence:** Power BI Desktop / Power BI Service (Despliegue e IA).
* **Control de Versiones:** Power BI Project (`.pbip`) + Git / GitHub.
* **Lenguaje Analítico:** DAX (`SWITCH`, iteraciones escalables sin sumas implícitas, filtrado dinámico).
* **UX/UI:** Paleta monocromática turquesa pastel con jerarquía cromática para niveles de riesgo (Treemap) y matriz de alta densidad.

---

## 📌 Hallazgos Clave de Negocio
1. **Concentración de Morosidad:** El segmento de **Riesgo Alto** presenta la Tasa de Default más crítica de la cartera con un **58,01%**, representando un capital expuesto significativo.
2. **Impacto por Tipo de Vivienda:** Los clientes en modalidad **RENT / OTHER** registran los mayores índices de morosidad, superando el 30% de impago general.
3. **Distribución Salarial:** A través del Treemap segmentado por `Rango_Salarial`, se identificó que el tramo de ingresos bajos requiere políticas de aprobación ajustadas por DTI.

---

## 💡 Capacidades de Inteligencia Artificial (Q&A)
Se integró un modelo lingüístico entrenado con sinónimos del negocio en Power BI Service que permite realizar consultas analíticas en lenguaje natural (ej. *"Mostrar la tasa de default en clientes con ingresos bajos"*).

---

## 📁 Estructura del Repositorio (.pbip)
```text
├── data/                    # Archivos de datos procesados y raw
├── power_bi/                # Archivos fuente del reporte Power BI (.pbip)
│   ├── *.Dataset/           # Modelado semántico y medidas DAX en JSON/BIM
│   └── *.Report/            # Definición visual y diseño de las páginas
├── .gitignore               # Exclusión de archivos temporales de Power BI
└── README.md                # Documentación del proyecto