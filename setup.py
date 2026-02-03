from setuptools import find_packages, setup

setup(
    name='cafesales_etl_project',
    packages=["src"],
    version='0.1.0',
    description='Pipeline ETL para Cafe Sales',
    author='Gabriel',
)
# ejecutar pip install -e .