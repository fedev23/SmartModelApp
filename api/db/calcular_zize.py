import sqlite3
import sqlite3

def estimar_tamano_bd_y_crecimiento(db_path):
    """
    Calcula un estimado del tamaño actual y futuro (doble) de las tablas en una base de datos SQLite.
    
    Args:
        db_path (str): Ruta al archivo de la base de datos SQLite.
    
    Returns:
        dict: Un diccionario con el nombre de cada tabla y su tamaño estimado actual y futuro (doble).
    """
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Obtener todas las tablas de la base de datos
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tablas = cursor.fetchall()
        
        # Tamaño promedio de los tipos de datos (en bytes)
        tipo_tamanos = {
            "INTEGER": 4,  # Depende del rango de valores
            "REAL": 8,
            "TEXT": 50,  # Tamaño promedio estimado para texto
            "BLOB": 100  # Tamaño promedio estimado para binarios
        }
        
        tamanos_tablas = {}
        
        for (tabla,) in tablas:
            # Obtener los nombres y tipos de las columnas de la tabla
            cursor.execute(f"PRAGMA table_info({tabla})")
            columnas = cursor.fetchall()
            
            # Calcular el tamaño promedio de una fila
            tamano_fila = 0
            for columna in columnas:
                col_type = columna[2].upper()  # Tipo de dato
                tamano_fila += tipo_tamanos.get(col_type, 4)  # Default: 4 bytes
            
            # Obtener el número de filas en la tabla
            cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
            num_filas = cursor.fetchone()[0]
            
            # Calcular el tamaño total estimado para la tabla
            tamano_total = tamano_fila * num_filas
            tamano_futuro = tamano_total * 2  # Crecimiento esperado al doble
            
            tamanos_tablas[tabla] = {
                "actual": tamano_total,
                "futuro": tamano_futuro
            }
        
        return tamanos_tablas
    
    except sqlite3.Error as e:
        print(f"Error al acceder a la base de datos: {e}")
        return None
    finally:
        if conn:
            conn.close()
            
            

db_path = "Modeling_App.db"
tamanos = estimar_tamano_bd_y_crecimiento(db_path)
if tamanos:
    total_actual = sum(tabla["actual"] for tabla in tamanos.values())
    total_futuro = sum(tabla["futuro"] for tabla in tamanos.values())
    
    print("\nTamaños estimados por tabla:")
    for tabla, valores in tamanos.items():
        print(f"Tabla: {tabla}, Tamaño actual: {valores['actual']} bytes, Tamaño futuro: {valores['futuro']} bytes")
    
    print(f"\nTamaño total actual: {total_actual} bytes")
    print(f"Tamaño total futuro (doble): {total_futuro} bytes")

def borrar_tablas(database_path, tablas):
    """
    Borra las tablas especificadas de una base de datos SQLite.

    :param database_path: Ruta al archivo de la base de datos.
    :param tablas: Lista de nombres de tablas a borrar.
    """
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()

        # Borrar cada tabla especificada
        for tabla in tablas:
            print(f"Borrando tabla: {tabla}")
            cur.execute(f"DROP TABLE IF EXISTS {tabla};")
        
        # Confirmar cambios
        conn.commit()
        print("Tablas borradas exitosamente.")
    except sqlite3.Error as e:
        print(f"Error al borrar tablas: {e}")
    finally:
        if conn:
            conn.close()

# Nombre de la base de datos
database_path = 'Modeling_App.db'

# Tablas a borrar
tablas_a_borrar = [
    "model_execution_backup",
    "model_execution_backup_json",
    "versiones_niveles_scorcad",
    "paths_de_ejecucion",
    "paths_de_ejecucion_niveles_scorcards",
    "paths_de_ejecucion_in_Sample"
]

# Llamar a la función para borrar tablas
#borrar_tablas(database_path, tablas_a_borrar)