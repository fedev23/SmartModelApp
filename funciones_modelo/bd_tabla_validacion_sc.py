

import sqlite3
from datetime import datetime
from api.db import *

def insert_validation_scoring(nombre_archivo, json_versiones_id, nombre_modelo):
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

    return insert_into_table("validation_scoring", columns, values)




import sqlite3

def obtener_ultimo_id_validation_scoring_por_json_version(json_versiones_id, database_path="Modeling_App.db"):
    """
    Obtiene el último ID utilizado en la tabla validation_scoring para un json_versiones_id específico, 
    basado en la columna 'ultima_vez_usado'.

    :param json_versiones_id: ID de la versión JSON a buscar.
    :param database_path: Ruta de la base de datos SQLite.
    :return: Diccionario con 'id_validacion_sc', 'json_versiones_id', 'version_id', 'nombre_modelo' o None si no hay registros.
    """
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        # Consulta SQL para obtener el último registro basado en 'ultima_vez_usado'
        query = """
            SELECT vs.id_validacion_sc, vs.json_versiones_id, jv.version_id, vs.nombre_modelo
            FROM validation_scoring vs
            JOIN json_versions jv ON vs.json_versiones_id = jv.id_jsons
            WHERE vs.json_versiones_id = ? AND vs.ultima_vez_usado IS NOT NULL
            ORDER BY datetime(vs.ultima_vez_usado) DESC
            LIMIT 1;
        """
        cursor.execute(query, (json_versiones_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                "id_validacion_sc": row[0],
                "json_versiones_id": row[1],
                "version_id": row[2],
                "nombre_modelo": row[3]
            }
        else:
            return None

    except sqlite3.Error as e:
        print(f"Error al obtener el último ID usado en validation_scoring para json_versiones_id={json_versiones_id}: {e}")
        return None


