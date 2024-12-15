import sqlite3


def obtener_estructura_tabla(database_path, tabla):
    """
    Obtiene la estructura de una tabla en la base de datos SQLite.

    :param database_path: Ruta al archivo de la base de datos.
    :param tabla: Nombre de la tabla cuya estructura deseas obtener.
    :return: Lista de diccionarios con la estructura de la tabla.
    """
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()

        # Consultar la estructura de la tabla
        cur.execute(f"PRAGMA table_info({tabla});")
        estructura = cur.fetchall()

        # Convertir los resultados en una lista de diccionarios
        estructura_list = [
            {
                "cid": col[0],  # Índice de la columna
                "name": col[1],  # Nombre de la columna
                "type": col[2],  # Tipo de dato
                "notnull": bool(col[3]),  # Si es NOT NULL
                "default_value": col[4],  # Valor por defecto
                "pk": bool(col[5]),  # Si es clave primaria
            }
            for col in estructura
        ]

        return estructura_list

    except sqlite3.Error as e:
        print(f"Error al obtener la estructura de la tabla '{tabla}': {e}")
        return []
    finally:
        conn.close()
        
        
database_path = "Modeling_App.db"
tabla = "json_versions"

estructura = obtener_estructura_tabla(database_path, tabla)

estructura = obtener_estructura_tabla(database_path, tabla)

if estructura:
    print(f"Estructura de la tabla '{tabla}':")
    for col in estructura:
        print(col)
else:
    print(f"No se pudo obtener la estructura de la tabla '{tabla}'.")