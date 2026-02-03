# ☕ Dirty Cafe Sales: From Chaos to Dashboard

![Status](https://img.shields.io/badge/STATUS-IN_PROGRESS-yellow?style=for-the-badge&logo=git)
![Python](https://img.shields.io/badge/PYTHON-3.12%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/PANDAS-DATA_CLEANING-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Power BI](https://img.shields.io/badge/POWER_BI-VISUALIZATION-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![DuckDB](https://img.shields.io/badge/DUCKDB-SQL_ANALYTICS-fff000?style=for-the-badge&logo=duckdb&logoColor=black)

## 📖 Sobre el Proyecto

Este proyecto simula un escenario real de **Data Engineering**: recibir un dataset "sucio" de ventas de una cadena de cafeterías, limpiarlo, modelarlo y construir un pipeline ETL robusto para alimentar un dashboard de negocio.

El objetivo principal es aplicar buenas prácticas de ingeniería de software (Clean Code, Type Hinting, Modularidad) al análisis de datos, alejándose de los scripts desordenados y acercándose a código listo para producción.

## 🗂️ Estructura del Proyecto

```text
cafe_etl_project/
│
├── data/
│   ├── raw/             # Dataset original (dirty_cafe_sales.csv)
│   ├── processed/       # Datos limpios intermedios
│   └── final/           # Tablas dimensionales (Parquet/CSV)
│
├── notebooks/           # Experimentación y EDA
├── src/                 # Código fuente productivo (ETL functions)
└── README.md            # Documentación del proyecto
