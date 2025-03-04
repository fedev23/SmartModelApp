import sqlite3
from datetime import datetime

# Conectar a la base de datos o crearla si no existe
conn = sqlite3.connect('Modeling_App.db')
cur = conn.cursor()

# Crear la tabla `project` con referencia a `user_id`
cur.execute('''
CREATE TABLE IF NOT EXISTS project (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    is_last_selected BOOLEAN DEFAULT 0
    created_date TEXT
)
''')

# Crear la tabla `execution_log` que referencia a `project`
cur.execute('''
CREATE TABLE IF NOT EXISTS execution_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    project_id INTEGER,
    execution_date TEXT,
    model_name TEXT,
    FOREIGN KEY (project_id) REFERENCES project(id)
)
''')

# Crear la tabla `model_execution` que referencia a `project`
cur.execute('''
CREATE TABLE IF NOT EXISTS model_execution (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            project_id INTEGER,
            execution_date TEXT,
            model_name TEXT,
            dataset_name TEXT,
            version_id INTEGER,  -- Nueva columna para la versión
            execution_id TEXT,
            model_type TEXT,
            execution_state TEXT DEFAULT 'pendiente',  -- Estado inicial del modelo
            FOREIGN KEY (project_id) REFERENCES project(id),
            FOREIGN KEY (version_id) REFERENCES versions(id)  -- Relación con la tabla 'versions'
        );
''')

# Crear la tabla `version` que referencia a `project`
cur.execute('''
CREATE TABLE IF NOT EXISTS version (
    version_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    nombre_version TEXT NOT NULL,
    execution_date TEXT,
    is_last_selected BOOLEAN DEFAULT 0
    FOREIGN KEY (project_id) REFERENCES project(id)
)
''')


cur.execute('''
            CREATE TABLE IF NOT EXISTS name_files (
                id_files INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_archivo TEXT NOT NULL,
                fecha_de_carga TEXT NOT NULL,
                project_id INTEGER,
                version_id INTEGER,
                is_last_selected BOOLEAN DEFAULT 0,
                FOREIGN KEY (project_id) REFERENCES project(id),
                FOREIGN KEY (version_id) REFERENCES version(version_id)
            )
        ''')

cur.execute('''
         CREATE TABLE json_versions (
                id_jsons INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_version TEXT NOT NULL,
                fecha_de_carga TEXT NOT NULL,
                version_id INTEGER,
                FOREIGN KEY (version_id) REFERENCES version(version_id)
            );
    ''')
    
cur.execute('''
       CREATE TABLE IF NOT EXISTS validation_scoring (
        id_validacion_sc INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_archivo_validation_sc TEXT NOT NULL,
        fecha_de_carga TEXT NOT NULL,
        version_id INTEGER,
        FOREIGN KEY (version_id) REFERENCES version(version_id)
    );
    ''')

##LA TENGO QUE BORRAR HACE REFERNECIA A JSON_VERSIO,
cur.execute('''
        CREATE TABLE IF NOT EXISTS  versiones_niveles_scorcad (
            id_version_niveles INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_version_niveles TEXT NOT NULL,
            project_id INTEGER,
            version_id INTEGER,
            FOREIGN KEY (project_id) REFERENCES project(id),
            FOREIGN KEY (version_id) REFERENCES version(version_id)
        );
    ''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS paths_de_ejecucion (
        id_path INTEGER PRIMARY KEY AUTOINCREMENT,
        path TEXT NOT NULL,
        project_id INTEGER,
        version_id INTEGER,
        FOREIGN KEY (project_id) REFERENCES project(id),
        FOREIGN KEY (version_id) REFERENCES version(version_id)
    );
''')

# Función para crear el índice único
def crear_indice_unico(conn):
    cur = conn.cursor()
    try:
        cur.execute('''
            CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_path 
            ON paths_de_ejecucion (path, project_id, version_id);
        ''')
        conn.commit()
        print("Índice único creado correctamente en paths_de_ejecucion.")
    except sqlite3.OperationalError as e:
        print(f"Error al crear el índice: {e}")



crear_indice_unico(conn)
def recreate_json_versions_table():
    conn = sqlite3.connect('Modeling_App.db')
    cur = conn.cursor()

    # Eliminar la tabla si existe
    cur.execute('''DROP TABLE IF EXISTS json_verions;''')

    # Crear la nueva tabla con la estructura correcta
    cur.execute('''
        CREATE TABLE json_versions (
            id_jsons INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_version TEXT NOT NULL,
            fecha_de_carga TEXT NOT NULL,
            project_id INTEGER,
            version_id INTEGER,
            FOREIGN KEY (project_id) REFERENCES project(id),
            FOREIGN KEY (version_id) REFERENCES version(version_id)
        );
    ''')

    # Confirmar cambios
    conn.commit()

    # Cerrar conexión
    conn.close()
    print("Tabla 'json_versions' recreada exitosamente.")


# Confirmar y cerrar la conexión
conn.commit()
conn.close()
print("Tablas creadas exitosamente en la base de datos.")

def list_tables():
    conn = sqlite3.connect('Modeling_App.db')
    cur = conn.cursor()
    
    # Listar todas las tablas
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()
    print("Tablas en la base de datos:", tables)
    
    conn.close()

# Llama a esta función para ver las tablas
#recreate_json_versions_table()
list_tables()
