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

# La imputación de datos es el método para completar la información faltante o no disponible en un conjunto de datos con otros números.
def impute_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rellena valores nulos usando lógica de negocio y elimina registros irrecuperables.
    
    :param df: DataFrame limpio (output de clean_data).
    :return: DataFrame listo para ingeniería de características.
    """

    df_imp = df.copy()
    initial_rows = len(df_imp)
    
    # Tenemos la fórmula: Total Spent = Price Per Unit * Quantity.
    # Si falta total_spent calcular si tenemos price_per_unit y quantity.
    df_imp["total_spent"] = df_imp["total_spent"].fillna(
        df_imp["price_per_unit"] * df_imp["quantity"]
    )
    
    # Si falta price_per_unit calcular si tenemos total_spent y quantity.
    df_imp["price_per_unit"] = df_imp["price_per_unit"].fillna(
        df_imp["total_spent"] / df_imp["quantity"]
    )
    
    # Imputación Categórica
    categorical_fills = {
        "payment_method": "Unknown",
        "location": "Unknown"
    }
    
    df_imp = df_imp.fillna(categorical_fills)
    

    # Sanity Check
    # Eliminamos si:
    # - No hay Fecha (Esencial para Time Series)
    # - No hay ID (Esencial para conteo)
    # - Siguen faltando datos financieros (Price/Total/Qty) después de imputar
    critical_cols = ["transaction_id", "transaction_date", "quantity", "price_per_unit", "total_spent"]
    
    df_imp = df_imp.dropna(subset=critical_cols)
    
    dropped_rows = initial_rows - len(df_imp)
    
    if dropped_rows > 0:
        logging.warning(f"Se eliminaron {dropped_rows} filas ({dropped_rows/initial_rows:.2%}) por falta de datos críticos.")
    else:
        logging.info("No se perdieron datos en la etapa de imputación.")
    
    return df_imp