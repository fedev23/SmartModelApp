import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('Modeling_App.db')
cur = conn.cursor()

# Crear la tabla `model_execution` para registrar ejecuciones de modelos
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

conn.commit()
conn.close()
print("Tabla 'model_execution' creada exitosamente en la base de datos.")
