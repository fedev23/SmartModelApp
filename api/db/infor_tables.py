import sqlite3
from typing import List, Tuple

def get_database_info(database_path: str) -> List[Tuple[str, str]]:
    """
    Recupera la lista de tablas y sus esquemas en la base de datos SQLite.

    Args:
        database_path (str): Ruta al archivo de la base de datos SQLite.

    Returns:
        List[Tuple[str, str]]: Lista de tuplas con el nombre de las tablas y sus esquemas.
    """
    try:
        # Conexión a la base de datos
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        # Obtener la lista de tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        # Obtener el esquema de cada tabla
        table_schemas = []
        for table_name in tables:
            table_name = table_name[0]
            cursor.execute(f"PRAGMA table_info({table_name});")
            schema_info = cursor.fetchall()
            table_schemas.append((table_name, schema_info))

        # Cerrar la conexión
        conn.close()

        return table_schemas
    except sqlite3.Error as e:
        print(f"Error al acceder a la base de datos: {e}")
        return []



database_path = "Modeling_App.db"
database_info = get_database_info(database_path)

if database_info:
    for table, schema in database_info:
        print(f"Tabla: {table}")
        print("Esquema:")
        for column in schema:
            print(column)
else:
    print("No se encontraron tablas o ocurrió un error.")
    
    

# Conectar a la base de datos (reemplaza 'tu_base_de_datos.db' con tu archivo de SQLite)
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

# Obtener las claves foráneas de la tabla validation_scoring
cursor.execute("PRAGMA foreign_key_list(model_execution);")
foreign_keys = cursor.fetchall()

# Mostrar los resultados
if foreign_keys:
    print("Claves foráneas en la tabla model_execution:")
    for fk in foreign_keys:
        print(f"Desde columna '{fk[3]}' -> Tabla Referenciada '{fk[2]}' en columna '{fk[4]}'")
else:
    print("No hay claves foráneas en la tabla model_execution.")

# Cerrar la conexión
conn.close()

    
    

    
