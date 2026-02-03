import pandas as pd
import logging
from typing import Optional

# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ingest_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Ingesta datos desde un CSV, normaliza headers y maneja valores nulos estándar.
    
    Args:
        file_path: Ruta absoluta o relativa al archivo CSV.
        
    Returns:
        pd.DataFrame: DataFrame con los datos crudos.
        
    Raises:
        FileNotFoundError: Si el archivo no existe.
    """
    try:
        df = pd.read_csv(
            file_path, 
            header=0,
            encoding="utf-8", 
            na_values=["ERROR", "UNKNOWN", "-", "null"],
            skipinitialspace=True
        )
        
        # Normalización de Headers (Quita espacios al inicio/final y convierte a minúsculas)
        df.columns = df.columns.str.strip()
    
        # Log Información exitosa
        logging.info(f"Ingestión exitosa. Dimensiones: {df.shape}")
        
        return df
    
    except FileNotFoundError:
        logging.error(f"Archivo no encontrado en: {file_path}")
    
    except Exception as e:
        logging.error(f"Error inesperado al ingerir datos: {e}")
        raise

    return None
