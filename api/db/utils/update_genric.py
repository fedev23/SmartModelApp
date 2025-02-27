import sqlite3
from datetime import datetime

def update_table(table_name, update_values, where_conditions, connection):
    """
    Realiza una actualización genérica en la base de datos.

    :param table_name: Nombre de la tabla en la que se hará el UPDATE.
    :param update_values: Diccionario con los valores a actualizar. Ejemplo: {"columna1": "valor1", "columna2": "valor2"}
    :param where_conditions: Diccionario con las condiciones para filtrar los registros a actualizar. Ejemplo: {"id": 5}
    :param connection: Objeto de conexión a la base de datos.
    :return: Cantidad de registros actualizados.
    """
    if not update_values:
        raise ValueError("Debe proporcionar al menos un valor para actualizar.")

    if not where_conditions:
        raise ValueError("Debe proporcionar al menos una condición para el WHERE.")

    # Construir la parte SET del UPDATE
    set_clause = ", ".join([f"{col} = ?" for col in update_values.keys()])
    
    # Construir la parte WHERE del UPDATE
    where_clause = " AND ".join([f"{col} = ?" for col in where_conditions.keys()])
    
    # Crear la consulta SQL
    query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
    
    # Obtener los valores en el orden correcto
    values = list(update_values.values()) + list(where_conditions.values())

    try:
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()
        return cursor.rowcount  # Retorna la cantidad de registros actualizados
    except sqlite3.Error as e:
        print(f"Error al actualizar la tabla {table_name}: {e}")
        return 0


