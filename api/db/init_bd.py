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
list_tables()


