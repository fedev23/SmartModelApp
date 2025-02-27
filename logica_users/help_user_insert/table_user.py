from api.db import *
import sqlite3

def insertar_usuario_user_info(hash_user_id, mail_user):
    """
    Inserta un nuevo usuario en la tabla 'user_info' con solo el hash_user_id y mail_user.

    :param hash_user_id: ID único del usuario.
    :param mail_user: Correo del usuario.
    :return: El ID del último registro insertado o None si hubo un error.
    """
    table_name = "user_info"
    columns = ["hash_user_id", "mail_user"]  # Columnas en la tabla
    values = [hash_user_id, mail_user]  # Valores a insertar

    # Llama a la función genérica para insertar
    return insert_into_table(table_name, columns, values)



def obtener_o_insertar_usuario(db_path, hash_user_id):
    """
    Inserta un hash_user_id en la tabla user_info si no existe y devuelve el ID del usuario.

    Parámetros:
        db_path (str): Ruta a la base de datos SQLite.
        hash_user_id (str): Hash del usuario a insertar.

    Retorna:
        int: ID del usuario en la tabla user_info.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Verificar si el usuario ya existe y obtener su ID
        cursor.execute("SELECT id FROM user_info WHERE hash_user_id = ?", (hash_user_id,))
        row = cursor.fetchone()

        if row:
            user_id = row[0]  # Usuario ya existente, devolver ID
            print(f"El usuario '{hash_user_id}' ya existe con ID {user_id}.")
        else:
            # Insertar nuevo usuario y obtener el ID generado automáticamente
            cursor.execute("INSERT INTO user_info (hash_user_id) VALUES (?)", (hash_user_id,))
            conn.commit()
            user_id = cursor.lastrowid  # Obtener el ID del último insertado
            print(f"Usuario '{hash_user_id}' insertado con ID {user_id}.")

        return user_id

    except sqlite3.Error as e:
        print(f"Error en la base de datos: {e}")
        return None
    finally:
        conn.close()