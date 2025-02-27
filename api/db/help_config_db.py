import sqlite3
from api.db import *

def insert_or_replace(db_path, table_name, data):
    """
    Inserta o reemplaza datos en una tabla de SQLite.

    :param db_path: Ruta a la base de datos SQLite.
    :param table_name: Nombre de la tabla.
    :param data: Diccionario donde las claves son los nombres de las columnas y los valores son los datos a insertar.
    """
    try:
        # Conexión a la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Construir la consulta dinámicamente
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        sql = f"INSERT OR REPLACE INTO {table_name} ({columns}) VALUES ({placeholders})"

        # Ejecutar la consulta
        cursor.execute(sql, tuple(data.values()))
        conn.commit()

        print(f"Datos insertados/reemplazados en la tabla '{table_name}': {data}")
    except sqlite3.Error as e:
        print(f"Error al insertar/reemplazar datos: {e}")
    finally:
        # Cerrar la conexión
        conn.close()
        
        
        

def insertar_configuracion_usuario_con_replace(db_path,
    user_id,
    valor_min_seg=None,
    valor_max_seg=None,
    num_select_filas=None,
    value_dark_or_light=None
):
    """
    Actualiza una configuración en la tabla 'user_configurations' basada en 'user_id'.
    Solo actualiza los valores proporcionados.

    :param db_path: Ruta a la base de datos SQLite.
    :param user_id: ID del usuario en 'user_configurations'.
    :param valor_min_seg: (Opcional) Valor mínimo de configuración.
    :param valor_max_seg: (Opcional) Valor máximo de configuración.
    :param num_select_filas: (Opcional) Número de filas seleccionadas.
    :param value_dark_or_light: (Opcional) Valor de configuración 'dark' o 'light'.
    :return: `True` si la actualización fue exitosa, `False` si falló.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Verificar si el user_id existe en user_configurations
        cursor.execute("SELECT 1 FROM user_configurations WHERE user_id = ?", (user_id,))
        existe_config = cursor.fetchone()

        if not existe_config:
            print(f"❌ No se encontró una configuración para user_id: {user_id}")
            return False

        # Construir la consulta dinámica
        updates = []
        params = []

        if valor_min_seg is not None:
            updates.append("valor_min_seg = ?")
            params.append(valor_min_seg)
        if valor_max_seg is not None:
            updates.append("valor_max_seg = ?")
            params.append(valor_max_seg)
        if num_select_filas is not None:
            updates.append("num_select_filas = ?")
            params.append(num_select_filas)
        if value_dark_or_light is not None:
            updates.append("value_dark_or_light = ?")
            params.append(value_dark_or_light)

        if updates:
            query = f"""
            UPDATE user_configurations
            SET {', '.join(updates)}
            WHERE user_id = ?;
            """
            params.append(user_id)
            cursor.execute(query, params)
            conn.commit()
            print(f"✅ Configuración actualizada para user_id: {user_id}.")
            return True
        else:
            print("⚠ No se proporcionaron valores para actualizar.")
            return False
    except sqlite3.Error as e:
        print(f"⚠ Error al actualizar la configuración: {e}")
        return False
    finally:
        conn.close()
        
                
def obtener_configuracion_por_hash(db_path, user_id):
    """
    Recupera los valores de configuración en 'user_configurations' utilizando 'user_id'.

    :param db_path: Ruta a la base de datos SQLite.
    :param user_id: Identificador único del usuario en 'user_configurations'.
    :return: Diccionario con los valores de configuración o None si no se encuentra.
    """
    # Definir la tabla y columnas para la consulta
    user_config_table = "user_configurations"
    user_config_columns = ["valor_min_seg", "valor_max_seg", "num_select_filas", "value_dark_or_light"]
    where_clause = "user_id = ?"
    where_params = (user_id,)

    # Se asume que existe una función get_records que realiza la consulta en la base de datos
    config_records = get_records(
        table=user_config_table,
        columns=user_config_columns,
        where_clause=where_clause,
        where_params=where_params
    )

    if not config_records:
        print(f"No se encontró configuración para user_id: {user_id}.")
        return None

    # Devolver el primer registro encontrado (asumiendo que solo hay uno por user_id)
    return config_records[0]



def insertar_usuario_si_no_existe(db_path, user_id):
    """
    Inserta un user_id en la tabla user_configurations si no existe, con valores predeterminados.

    Parámetros:
        db_path (str): Ruta a la base de datos SQLite.
        user_id (int): ID del usuario.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Verificar si el user_id ya existe
        cursor.execute("SELECT 1 FROM user_configurations WHERE user_id = ?", (user_id,))
        existe = cursor.fetchone()

        # Si no existe, insertarlo con valores predeterminados
        if not existe:
            cursor.execute("""
                INSERT INTO user_configurations 
                (user_id, valor_min_seg, valor_max_seg, num_select_filas, value_dark_or_light)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, 3, 8, 5, "light"))  # Valores predeterminados

            conn.commit()
            print(f"Usuario {user_id} insertado correctamente en user_configurations.")
        else:
            print(f"El usuario {user_id} ya existe en user_configurations.")

    except sqlite3.Error as e:
        print(f"Error en la base de datos: {e}")
    finally:
        conn.close()