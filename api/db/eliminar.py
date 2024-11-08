import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('Modeling_App.db')
cur = conn.cursor()

# Eliminar la tabla `version` si ya existe
cur.execute('DROP TABLE IF EXISTS version')

# Volver a crear la tabla `version` con el campo `execution_time`
cur.execute('''
CREATE TABLE version (
    version_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    nombre_version TEXT NOT NULL,
    execution_date TEXT,
    FOREIGN KEY (project_id) REFERENCES project(id)
)
''')

# Confirmar y cerrar la conexión
conn.commit()
conn.close()
print("Tabla `version` eliminada y recreada con éxito.")
