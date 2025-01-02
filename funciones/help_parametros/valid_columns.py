import pandas as pd

def get_categorical_columns_with_unique_values_range(dataset, min_unique=3, max_unique=8):
    """
    Devuelve las columnas categóricas que tienen entre un rango específico de valores únicos.

    :param dataset: DataFrame que contiene los datos.
    :param min_unique: Mínimo número de valores únicos (inclusive).
    :param max_unique: Máximo número de valores únicos (inclusive).
    :return: Lista de las columnas categóricas que cumplen con el rango de valores únicos.
    """
    if dataset.empty:
        print("El dataset está vacío.")
        return []

    # Filtrar columnas categóricas
    categorical_columns = dataset.select_dtypes(include=['object', 'category'])
    print(f"Columnas categóricas detectadas: {categorical_columns.columns.tolist()}")

    if categorical_columns.empty:
        print("No hay columnas categóricas en el dataset.")
        return []

    # Filtrar columnas categóricas por rango de valores únicos
    columns_in_range = [
        col for col in categorical_columns.columns
        if min_unique <= categorical_columns[col].nunique() <= max_unique
    ]    

    return columns_in_range