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
    FOREIGN KEY (project_id) REFERENCES project(id)
)
''')

# Crear la tabla `version` que referencia a `project`
cur.execute('''
CREATE TABLE IF NOT EXISTS version (
    version_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    nombre_version TEXT NOT NULL,
    execution_date TEXT,
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
                FOREIGN KEY (project_id) REFERENCES project(id),
                FOREIGN KEY (version_id) REFERENCES version(version_id)
            )
        ''')

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
#list_tables()
