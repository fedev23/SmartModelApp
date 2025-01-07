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


def get_binary_columns(df):
    """
    Devuelve una lista de columnas que contienen exclusivamente los valores 0 y 1.

    :param df: DataFrame que contiene los datos.
    :return: Lista de nombres de las columnas que tienen solo valores 0 y 1.
    """
    binary_columns = []

    for col in df.columns:
        # Verifica si la columna contiene únicamente los valores 0 y 1
        if df[col].dropna().isin([0, 1]).all():
            binary_columns.append(col)

    return binary_columns


def identificar_columnas_id(dataset: pd.DataFrame, umbral_unicidad: float = 0.9):
    """
    Identifica columnas identificadoras en un dataset mejorando la precisión.
    
    Parámetros:
    - dataset (pd.DataFrame): El DataFrame que se analizará.
    - umbral_unicidad (float): Proporción mínima de valores únicos respecto al total
      de filas para considerar una columna como identificadora (valor entre 0 y 1).
    
    Retorna:
    - dict: Un diccionario con:
      - "columnas_identificadoras": Columnas que tienen valores completamente únicos.
      - "columnas_posibles": Columnas con alta unicidad o candidatas como identificadores.
    """
    columnas_identificadoras = []
    columnas_posibles = []

    for columna in dataset.columns:
        # Ignorar valores nulos
        valores_unicos = dataset[columna].dropna().nunique()
        total_filas = len(dataset[columna].dropna())
        
        if total_filas == 0:  # Si no hay datos en la columna, saltar
            continue

        # Verificar unicidad completa
        if valores_unicos == total_filas:
            columnas_identificadoras.append(columna)
        # Verificar alta proporción de unicidad
        elif valores_unicos / total_filas >= umbral_unicidad:
            columnas_posibles.append(columna)

    return {
        "columnas_identificadoras": columnas_identificadoras,
        "columnas_posibles": columnas_posibles
    }
