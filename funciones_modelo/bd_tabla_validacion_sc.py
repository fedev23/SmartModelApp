

import sqlite3
from datetime import datetime
from api.db import *

def insert_validation_scoring(table_name, nombre_archivo, json_versiones_id, nombre_modelo):
    """
    Inserta un nuevo registro en la tabla validation_scoring utilizando la función insert_into_table.

    :param nombre_archivo: Nombre del archivo de validación scoring.
    :param json_versiones_id: ID de la versión JSON asociada.
    :param nombre_modelo: Tipo de modelo ('validacion' o 'scoring').
    :return: El ID del último registro insertado o None si hubo un error.
    """
    # Verificar que json_versiones_id no sea None
    if json_versiones_id is None:
        raise ValueError("El campo 'json_versiones_id' no puede ser None")

    # Generar la fecha de carga y última vez usado
    
    fecha_carga = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ultima_vez_usado = fecha_carga  # Se considera el último uso al momento de la inserción

    # Insertar en la base de datos usando la función insert_into_table
    columns = ["nombre_archivo_validation_sc", "fecha_de_carga", "json_versiones_id", "ultima_vez_usado", "nombre_modelo"]
    values = [nombre_archivo, fecha_carga, json_versiones_id, ultima_vez_usado, nombre_modelo]

    return insert_into_table(table_name, columns, values)



def insert_scoring(table_name, nombre_archivo, json_versiones_id, nombre_modelo):
    """
    Inserta un nuevo registro en la tabla validation_scoring utilizando la función insert_into_table.

    :param nombre_archivo: Nombre del archivo de validación scoring.
    :param json_versiones_id: ID de la versión JSON asociada.
    :param nombre_modelo: Tipo de modelo ('validacion' o 'scoring').
    :return: El ID del último registro insertado o None si hubo un error.
    """
    # Verificar que json_versiones_id no sea None
    if json_versiones_id is None:
        raise ValueError("El campo 'json_versiones_id' no puede ser None")

    # Generar la fecha de carga y última vez usado
    
    fecha_carga = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ultima_vez_usado = fecha_carga  # Se considera el último uso al momento de la inserción

    # Insertar en la base de datos usando la función insert_into_table
    columns = ["nombre_dataset", "fecha_de_carga", "json_versiones_id", "ultima_vez_usado", "model_name"]
    values = [nombre_archivo, fecha_carga, json_versiones_id, ultima_vez_usado, nombre_modelo]

    return insert_into_table(table_name, columns, values)


def obtener_ultimo_id_validation_scoring_por_json_version(json_versiones_id, tabla, database_path="Modeling_App.db"):
    """
    Obtiene el último ID utilizado en una tabla específica para un json_versiones_id dado,
    basado en la columna 'ultima_vez_usado'.

    :param json_versiones_id: ID de la versión JSON a buscar.
    :param tabla: Nombre de la tabla a consultar ('validation_scoring' o 'scoring').
    :param database_path: Ruta de la base de datos SQLite.
    :return: ID del último registro o None si no hay registros.
    """
    if tabla not in ("validation_scoring", "scoring"):
        raise ValueError("Tabla no válida. Debe ser 'validation_scoring' o 'scoring'.")

    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        # Determinar el nombre de la columna ID dependiendo de la tabla
        id_columna = "id_validacion_sc" if tabla == "validation_scoring" else "id_score"

        query = f"""
            SELECT {tabla}.{id_columna}
            FROM {tabla}
            WHERE {tabla}.json_versiones_id = ? AND {tabla}.ultima_vez_usado IS NOT NULL
            ORDER BY datetime({tabla}.ultima_vez_usado) DESC
            LIMIT 1;
        """

        cursor.execute(query, (json_versiones_id,))
        row = cursor.fetchone()
        conn.close()

        return row[0] if row else None

    except sqlite3.Error as e:
        print(f"Error al obtener el último ID en la tabla {tabla} para json_versiones_id={json_versiones_id}: {e}")
        return None
    
    
    
def obtener_ultimo_id_scoring(json_versiones_id, database_path="Modeling_App.db"):
    """
    Obtiene el último ID utilizado en la tabla 'scoring' para un json_versiones_id dado,
    basado en la columna 'ultima_vez_usado'.

    :param json_versiones_id: ID de la versión JSON a buscar.
    :param database_path: Ruta de la base de datos SQLite.
    :return: ID del último registro usado o None si no hay registros.
    """
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        query = """
            SELECT id_score
            FROM scoring 
            WHERE json_versiones_id = ? AND ultima_vez_usado IS NOT NULL
            ORDER BY datetime(ultima_vez_usado) DESC
            LIMIT 1;
        """

        cursor.execute(query, (json_versiones_id,))
        row = cursor.fetchone()
        conn.close()

        return row[0] if row else None

    except sqlite3.Error as e:
        print(f"Error al obtener el último ID en la tabla 'scoring' para json_versiones_id={json_versiones_id}: {e}")
        return None


