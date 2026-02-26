"""
Archivo de configuración para empaquetar el proyecto ETL.
Permite que la carpeta 'src' sea reconocida como un módulo instalable de Python,
solucionando el problema de 'ModuleNotFoundError' al importar desde los notebooks.
"""

from setuptools import find_packages, setup

setup(
    # Nombre interno del paquete (cómo lo registrará pip en tu entorno virtual)
    name='cafesales_etl_project',
    
    # Define qué carpetas contienen el código fuente importable.
    # Al pasar ["src"], le decimos explícitamente que solo convierta 
    # esa carpeta en un módulo (requiere que src/ tenga un __init__.py)
    packages=["src"],
    # (Alternativa dinámica): packages=find_packages(),

    # Versión actual del proyecto (Sigue el formato Mayor.Menor.Parche)
    version='0.1.0',
    
    # Breve descripción para documentación
    description='Pipeline ETL para Cafe Sales',
    
    # Autor o creador del paquete
    author='Gabriel',
    
    # se podríasagregar dependencias si quiero que se instalen solas
    # install_requires=[
    #     'pandas',
    #     'pathlib'
    # ],
)
# Instrucción de uso: 
# Abrir la terminal, asegurar que el entorno virtual (.env) esté activo, y ejecutar:
# pip install -e .