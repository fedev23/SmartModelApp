from api.db import *

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
