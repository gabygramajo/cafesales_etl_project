import pandas as pd
from pathlib import Path
import logging
from src.etl_functions import ingest_data, clean_data, impute_data, temporal_features

# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    
    logging.info(f"Iniciando pipeline ETL")
    
    try:
        # raíz del proyecto
        project_root = Path(__file__).resolve().parent
        
        # Definición de rutas
        bronze_file = project_root / "data" / "bronze" / "dirty_cafe_sales.csv"
        silver_dir = project_root / "data" / "silver"
        silver_csv_path = silver_dir / "clean_cafe_sales.csv"
        
        # Nos aseguramos de que la carpeta silver exista
        silver_dir.mkdir(parents=True, exist_ok=True)

        # EXTRACT
        logging.info(f"Leyendo datos crudos desde: {bronze_file.name}")
        df_cafe_sales = ingest_data(bronze_file)

        # TRANSFORM
        logging.info("Aplicando transformaciones y limpieza de datos...")
        df_cafe_sales_cleaned = clean_data(df_cafe_sales)
        df_cafe_sales_cleaned = impute_data(df_cafe_sales_cleaned)
        df_cafe_sales_cleaned = temporal_features(df_cafe_sales_cleaned)

        # LOAD
        logging.info(f"Cargando datos limpios en Capa Silver: {silver_csv_path.name}")
        df_cafe_sales_cleaned.to_csv(silver_csv_path, index=False)
        
        logging.info("Pipeline finalizado con éxito.")

    except Exception as e:
        # Si algo falla, el pipeline no solo se rompe, sino que documenta el porqué
        logging.error(f"Error crítico en el pipeline ETL: {e}")


if __name__ == "__main__":
    main()