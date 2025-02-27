import sqlite3

def recreate_table(database_path, table_name, create_table_sql):
    """
    Recreate a table in an SQLite database by dropping it and creating it again with a new structure.

    Args:
        database_path (str): Path to the SQLite database file.
        table_name (str): Name of the table to be recreated.
        create_table_sql (str): SQL statement to create the table with the desired structure.

    Returns:
        None
    """
    try:
        # Connect to the database
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()

        # Disable foreign key constraints temporarily
        cur.execute('PRAGMA foreign_keys=OFF;')

        # Drop the existing table if it exists
        cur.execute(f'DROP TABLE IF EXISTS {table_name};')

        # Recreate the table with the new structure
        cur.execute(create_table_sql)

        # Commit the changes
        conn.commit()
        print(f"Table '{table_name}' recreated successfully.")

    except sqlite3.Error as e:
        print(f"Error recreating table '{table_name}': {e}")
    finally:
        conn.close()


# Recreate the 'name_files' table
def recreate_name_files_table(database_path):
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS name_files (
        id_files INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_archivo TEXT NOT NULL,
        fecha_de_carga TEXT NOT NULL,
        version_id INTEGER,
        is_last_selected BOOLEAN DEFAULT 0,
        FOREIGN KEY (version_id) REFERENCES version(version_id)
    );
    '''
    recreate_table(database_path, 'name_files', create_table_sql)


# Recreate the 'validation_scoring' table
def recreate_validation_scoring_table(database_path):
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS validation_scoring (
        id_validacion_sc INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_archivo_validation_sc TEXT NOT NULL,
        fecha_de_carga TEXT NOT NULL,
        version_id INTEGER,
        FOREIGN KEY (version_id) REFERENCES version(version_id)
    );
    '''
    recreate_table(database_path, 'validation_scoring', create_table_sql)


# Recreate the 'versiones_niveles_scorcad' table
def recreate_versiones_niveles_scorcad_table(database_path):
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS versiones_niveles_scorcad (
        id_version_niveles INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_version_niveles TEXT NOT NULL,
        version_id INTEGER,
        FOREIGN KEY (version_id) REFERENCES version(version_id)
    );
    '''
    recreate_table(database_path, 'versiones_niveles_scorcad', create_table_sql)


# Recreate the 'paths_de_ejecucion' table
def recreate_paths_de_ejecucion_table(database_path):
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS paths_de_ejecucion (
        id_path INTEGER PRIMARY KEY AUTOINCREMENT,
        path TEXT NOT NULL,
        version_id INTEGER,
        FOREIGN KEY (version_id) REFERENCES version(version_id)
    );
    '''
    recreate_table(database_path, 'paths_de_ejecucion', create_table_sql)
    

# Ruta a la base de datos SQLite
database_path = 'Modeling_App.db'


#recreate_paths_de_ejecucion_in_sample_table(database_path)
# Recrear cada tabla
#recreate_name_files_table(database_path)
#recreate_validation_scoring_table(database_path)
#recreate_versiones_niveles_scorcad_table(database_path)
#recreate_paths_de_ejecucion_table(database_path)


def inspect_references(database_path, table_name):
    """
    Inspects the foreign key references of a given table in an SQLite database.

    :param database_path: Path to the SQLite database file.
    :param table_name: Name of the table to inspect.
    :return: A list of dictionaries with foreign key details.
    """
    try:
        # Conexión a la base de datos
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        # Obtener las claves foráneas de la tabla
        cursor.execute(f"PRAGMA foreign_key_list({table_name});")
        foreign_keys = cursor.fetchall()
        conn.close()

        # Formatear los resultados
        fk_info = [
            {
                "id": fk[0],  # ID de la clave foránea
                "table": fk[2],  # Tabla referenciada
                "from": fk[3],  # Columna en la tabla actual
                "to": fk[4],  # Columna en la tabla referenciada
                "on_update": fk[5],  # Acción al actualizar
                "on_delete": fk[6],  # Acción al eliminar
            }
            for fk in foreign_keys
        ]

        return fk_info

    except sqlite3.Error as e:
        print(f"Error al acceder a la base de datos: {e}")
        return None

        
        

def add_indexes_to_columns(conn, table_name, columns):
    """
    Crea índices en la tabla especificada para cada columna en la lista `columns`.
    
    Args:
        conn (sqlite3.Connection): Conexión a la base de datos SQLite.
        table_name (str): Nombre de la tabla en la que se crearán los índices.
        columns (list): Lista de nombres de columnas a indexar.
    
    Ejemplo de uso:
        add_indexes_to_columns(conn, 'json_versions', ['id_jsons', 'version_id'])
    """
    try:
        cur = conn.cursor()
        # Inicia una transacción
        cur.execute("BEGIN TRANSACTION;")
        
        for col in columns:
            # Se construye el nombre del índice, por ejemplo: idx_json_versions_id_jsons
            index_name = f"idx_{table_name}_{col}"
            # Construcción de la sentencia SQL para crear el índice
            query = f"CREATE INDEX IF NOT EXISTS {index_name} ON {table_name}({col});"
            cur.execute(query)
        
        # Finaliza la transacción
        conn.commit()
        print("Índices creados exitosamente.")
        
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Error al crear índices: {e}")

# Conexión a la base de datos (asegúrate de que 'mi_base_de_datos.sqlite' exista o se cree)
db_file = "Modeling_App.db"
conn = sqlite3.connect(db_file)

# Nombre de la tabla y columnas que se desean indexar
table = "project"
columns_to_index = ["id", "user_id"]

# Llamada a la función para crear los índices
add_indexes_to_columns(conn, table, columns_to_index)

# Cerrar la conexión a la base de datos
conn.close()
