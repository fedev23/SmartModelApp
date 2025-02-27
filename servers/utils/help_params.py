def split_list(input_list):
    """
    Función que separa el primer valor de una lista en una variable y los demás valores en otra.

    Parámetros:
        input_list (list): La lista de entrada.

    Retorna:
        tuple: Una tupla con el primer valor y los valores restantes como dos elementos separados.
    """
    if not input_list or len(input_list) == 0:
        return None, []

    first_value = input_list[0]
    remaining_values = input_list[1:]

    return first_value, remaining_values




def update_dataframe(df, split_values):
    """
    Actualiza un DataFrame separando el primer valor antes de una coma y el resto después, 
    o utiliza valores proporcionados explícitamente en split_values.

    Parámetros:
        df (pd.DataFrame): DataFrame con una columna llamada "Variables de corte".
        split_values (list): Lista de listas con valores separados.

    Retorna:
        pd.DataFrame: DataFrame actualizado con dos columnas, "Primer valor" y "Resto valores".
    """
    primer_valores = []
    resto_valores = []

    for valores in split_values:
        first_value, remaining_values = split_list(valores)
        primer_valores.append(first_value)
        resto_valores.append(", ".join(remaining_values))

    df["Primer valor"] = primer_valores
    df["Resto valores"] = resto_valores

    return df
