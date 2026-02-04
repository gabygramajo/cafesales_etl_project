import pandas as pd
import logging
from typing import Optional

# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ingest_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Ingesta datos desde un CSV, normaliza headers y maneja valores nulos estándar.
    
    :param file_path: Ruta absoluta o relativa al archivo CSV.
    :type file_path: str
    :return: DataFrame con los datos crudos
    :rtype: DataFrame | None
    :raises FileNotFoundError: Si el archivo no existe.
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

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Realiza limpieza exhaustiva: estandariza headers, fechas, strings y tipos numéricos.
    
    :param df: DataFrame con los datos crudos.
    :type df: pd.DataFrame
    :return: DataFrame con los datos limpios.
    :rtype: DataFrame
    """
    
    df_clean = df.copy()
    
    # normalizanción de headers (Snake Case)
    df_clean.columns = df_clean.columns \
                .str.strip() \
                .str.lower() \
                .str.replace(' ', '_')
    
    # normalizar fechas
    df_clean["transaction_date"] = pd.to_datetime(
        df_clean["transaction_date"], 
        format='%Y-%m-%d', 
        errors='coerce'
    )
  
    # normalizar texto de columnas tipo str
    text_cols = ["item", "payment_method", "location"]
    
    for col in text_cols:
        # .str accessor respeta los NaNs automáticamente
        df_clean[col] = df_clean[col].str.strip().str.title()
    
    # nomalizar columnas de enteros a Int64
    df_clean["quantity"] = pd.to_numeric(df_clean["quantity"], errors='coerce').astype('Int64')
    
    # nomalizar columnas de flotantes a float64
    money_cols = ["price_per_unit", "total_spent"]
    
    for col in money_cols:
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').astype('float64')
      
    logging.info(f"Limpieza completada. Nulos en fechas: {df_clean['transaction_date'].isna().sum()}")
    
    return df_clean