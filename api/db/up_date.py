import sqlite3
from datetime import datetime
from api.db import *

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




def insertar_nombre_file(nombre_file, id_proyecto, database_path="Modeling_App.db"):
    """
    Inserta un nuevo archivo en la tabla 'nombre_files', asociándolo a un proyecto,
    y devuelve el último ID insertado.
    
    :param nombre_file: Nombre del archivo a insertar.
    :param id_proyecto: ID del proyecto asociado (puede ser None).
    :param database_path: Ruta de la base de datos SQLite.
    :return: ID del último registro insertado o None si hubo un error.
    """
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        fecha_cargado = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Ejecutar la inserción
        cursor.execute("""
            INSERT INTO nombre_files (nombre_file, fecha_cargado, id_proyecto)
            VALUES (?, ?, ?);
        """, (nombre_file, fecha_cargado, id_proyecto))

        # Obtener el último ID insertado
        ultimo_id = cursor.lastrowid

        # Confirmar la inserción y cerrar la conexión
        conn.commit()
        conn.close()
        
        print(f"✅ Archivo '{nombre_file}' insertado correctamente en 'nombre_files' con ID {ultimo_id}.")
        return ultimo_id

    except sqlite3.Error as e:
        print(f"❌ Error al insertar en 'nombre_files': {e}")
        return None
    
    
def insertar_nombre_file_desa_insa(db_path, columns, values):
    """
    Inserta datos en la tabla 'name_files' de forma dinámica.

    Parámetros:
    - db_path (str): Ruta de la base de datos SQLite.
    - columns (list): Lista de nombres de columnas a insertar.
    - values (list): Lista de valores correspondientes a las columnas.

    Retorna:
    - bool: True si la inserción fue exitosa, False si hubo un error.
    """
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Crear la consulta SQL dinámica
        columns_str = ", ".join(columns)  # Convierte la lista en 'nombre_archivo, fecha_de_carga, project_id'
        placeholders = ", ".join(["?"] * len(values))  # Crea los placeholders (?, ?, ?)
        query = f"INSERT INTO name_files ({columns_str}) VALUES ({placeholders})"

        # Ejecutar la consulta con los valores proporcionados
        cursor.execute(query, values)

        # Confirmar la transacción
        conn.commit()
        print(f"✅ Registro insertado correctamente en 'name_files': {values}")

        return True

    except sqlite3.Error as e:
        print(f"❌ Error al insertar en 'name_files': {e}")
        return False

    finally:
        # Cerrar la conexión
        if conn:
            conn.close()


def obtener_nombres_files_por_proyecto(id_proyecto):
    """
    Recupera los nombres de archivos almacenados en la tabla 'nombre_files' 
    filtrados por el ID del proyecto.

    :param id_proyecto: ID del proyecto cuyos archivos se quieren recuperar.
    :return: Lista de diccionarios con los registros de la tabla 'nombre_files' para el proyecto dado.
    """
    # Especificamos las columnas que queremos recuperar
    columnas = ["id_nombre_file", "nombre_file", "fecha_cargado", "id_proyecto"]
    
    # Definimos la condición WHERE para filtrar por el ID del proyecto
    where_clause = "id_proyecto = ?"
    
    # Llamamos a la función get_records con la condición WHERE
    return get_records("nombre_files", columnas, where_clause=where_clause, where_params=(id_proyecto,))


def obtener_nombre_file(base_datos, id_nombre_file):
    """
    Obtiene el nombre de un archivo en la tabla 'nombre_files' filtrando por su ID.

    Args:
        base_datos (str): Ruta a la base de datos SQLite.
        id_nombre_file (int): ID del archivo a buscar.

    Returns:
        str: Nombre del archivo si se encuentra, o None si no existe.
    """
    conn = sqlite3.connect(base_datos)
    
    try:
        cursor = conn.cursor()
        
        # Consulta SQL para obtener el nombre del archivo
        query = """
        SELECT nombre_file 
        FROM nombre_files 
        WHERE id_nombre_file = ?
        """
        cursor.execute(query, (id_nombre_file,))
        
        # Obtener el resultado
        resultado = cursor.fetchone()
        
        return resultado[0] if resultado else None  # Retorna el nombre del archivo o None si no existe

    except sqlite3.Error as e:
        print(f"❌ Error al acceder a la base de datos: {e}")
        return None

    finally:
        conn.close()  # Cerrar la conexión

        conn.close()  # Cerrar la conexión



def obtener_ultimo_id_file_por_validacion(id_validacion_sc):
    """
    Obtiene el último 'id_nombre_file' en la tabla 'validation_scoring' para un ID de validación específico.

    Args:
        id_validacion_sc (int): ID de la validación para filtrar los registros.

    Returns:
        dict: Diccionario con el 'id_validacion_sc', el 'nombre_modelo' y el último 'id_nombre_file'.
        None: Si no hay datos en la tabla para ese ID de validación.
    """
    conn = sqlite3.connect("Modeling_App.db")  # Conectar a la base de datos
    cursor = conn.cursor()

    try:
        # Obtener el último id_nombre_file para ese id_validacion_sc ordenado por fecha de ejecución
        cursor.execute("""
            SELECT nombre_modelo, id_validacion_sc, id_nombre_file
            FROM validation_scoring
            WHERE id_validacion_sc = ?
            ORDER BY datetime(fecha_de_ejecucion) DESC
            LIMIT 1
        """, (id_validacion_sc,))

        ultimo_modelo = cursor.fetchone()

        if not ultimo_modelo:
            print(f"No hay registros en validation_scoring para la validación {id_validacion_sc}.")
            return None

        nombre_modelo, id_validacion_sc, id_nombre_file = ultimo_modelo

        return {
            "id_validacion_sc": id_validacion_sc,
            "nombre_modelo": nombre_modelo,
            "id_nombre_file": id_nombre_file
        }

    except sqlite3.Error as e:
        print(f"Error al obtener el último id_nombre_file para la validación {id_validacion_sc}: {e}")
        return None

    finally:
        conn.close()    


        

def obtener_ultimo_id_de_validacion_full_por_id_data_y_version(id_nombre_file, json_versiones_id):
    """
    Obtiene el último ID de validación (id_validacion_sc) en la tabla 'validation_scoring'
    a partir del ID del dataset (id_nombre_file) y la versión de niveles (json_versiones_id).

    Args:
        id_nombre_file (int): ID del dataset.
        json_versiones_id (int): ID de la versión de niveles asociada.

    Returns:
        int: ID de validación si se encuentra.
        None: Si no hay registros asociados a ese dataset y versión de niveles.
    """
    conn = sqlite3.connect("Modeling_App.db")
    cursor = conn.cursor()

    try:
        print(f"Buscando validación para dataset {id_nombre_file} y versión {json_versiones_id}...")

        # Consulta para obtener el último id_validacion_sc basado en id_nombre_file y json_versiones_id
        query = """
            SELECT id_validacion_sc
            FROM validation_scoring
            WHERE id_nombre_file = ? AND json_versiones_id = ?
            ORDER BY datetime(fecha_de_ejecucion) DESC
            LIMIT 1;
        """
        print(f"Ejecutando consulta: {query}")
        print(f"Valores: ({id_nombre_file}, {json_versiones_id})")

        cursor.execute(query, (id_nombre_file, json_versiones_id))
        resultado = cursor.fetchone()

        print(f"Resultado obtenido: {resultado}")

        return resultado[0] if resultado else None

    except sqlite3.Error as e:
        print(f"Error al obtener el id_validacion_sc para dataset {id_nombre_file} y versión {json_versiones_id}: {e}")
        return None

    finally:
        conn.close()  
        


def obtener_ultimo_id_file_scoring(id_proyecto):
    """
    Obtiene el último modelo generado en la tabla 'scoring' dentro de un proyecto específico
    y retorna el último 'id_nombre_file' vinculado a ese modelo.

    Args:
        id_proyecto (int): ID del proyecto para filtrar los modelos.

    Returns:
        dict: Diccionario con el último modelo generado dentro del proyecto y su 'id_nombre_file'.
        None: Si no hay datos en la tabla para ese proyecto.
    """
    conn = sqlite3.connect("Modeling_App.db")  # Conectar a la base de datos
    cursor = conn.cursor()

    try:
        # Obtener el último modelo generado para ese proyecto
        cursor.execute("""
            SELECT s.model_name, s.id_score, s.id_nombre_file
            FROM scoring s
            JOIN nombre_files nf ON s.id_nombre_file = nf.id_nombre_file
            WHERE nf.id_proyecto = ?
            ORDER BY datetime(s.fecha_de_ejecucion) DESC
            LIMIT 1
        """, (id_proyecto,))

        ultimo_modelo = cursor.fetchone()

        if not ultimo_modelo:
            print(f"No hay modelos generados para el proyecto {id_proyecto}.")
            return None

        nombre_modelo, id_score, id_nombre_file = ultimo_modelo

        return {
            "id_proyecto": id_proyecto,
            "nombre_modelo": nombre_modelo,
            "id_score": id_score,
            "id_nombre_file": id_nombre_file
        }

    except sqlite3.Error as e:
        print(f"Error al obtener el último modelo y su id_nombre_file para el proyecto {id_proyecto}: {e}")
        return None

    finally:
        conn.close()
