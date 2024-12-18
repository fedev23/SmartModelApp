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
        
 
    


def verificar_datos():
    """
    Verifica los datos entre las tablas json_versions y version.
    """
    try:
        # Conectarse a la base de datos SQLite
        conn = sqlite3.connect('Modeling_App.db')
        cur = conn.cursor()
        
        # Consulta SQL para verificar la relación entre las tablas
        query = '''
            SELECT j.id_jsons, j.nombre_version, j.version_id, v.project_id
            FROM json_versions j
            JOIN version v ON j.version_id = v.version_id;
        '''
        
        # Ejecutar la consulta
        cur.execute(query)
        
        # Obtener los resultados
        resultados = cur.fetchall()
        
        # Mostrar los resultados en formato tabular
        print("Resultados de la consulta:")
        print(f"{'id_jsons':<10} {'nombre_version':<20} {'version_id':<10} {'project_id':<10}")
        print("-" * 60)
        for row in resultados:
            print(f"{row[0]:<10} {row[1]:<20} {row[2]:<10} {row[3]:<10}")
    
    except sqlite3.Error as e:
        print(f"Error al ejecutar la consulta: {e}")
    
    finally:
        # Cerrar la conexión a la base de datos
        conn.close()

# Ejecutar la función
verificar_datos()


import sqlite3

def verificar_sql_manual():
    """
    Ejecuta manualmente la consulta SQL para verificar los filtros.
    """
    conn = sqlite3.connect('Modeling_App.db')
    cur = conn.cursor()

    project_id = 57  # ID del proyecto
    version_id = 30  # ID de la versión específica

    try:
        query = '''
            SELECT j.id_jsons, j.nombre_version, j.version_id
            FROM json_versions j
            INNER JOIN version v ON j.version_id = v.version_id
            WHERE v.project_id = ? AND j.version_id = ?
        '''
        print("Consulta SQL:", query)
        print("Parámetros:", (project_id, version_id))
        
        cur.execute(query, (project_id, version_id))
        resultados = cur.fetchall()

        print("\nResultados filtrados:")
        print(f"{'id_jsons':<10} {'nombre_version':<20} {'version_id':<10}")
        print("-" * 50)
        for row in resultados:
            print(f"{row[0]:<10} {row[1]:<20} {row[2]:<10}")

    except sqlite3.Error as e:
        print(f"Error en la consulta SQL: {e}")
    finally:
        conn.close()

# Ejecutar la verificación
verificar_sql_manual()
