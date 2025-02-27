import sqlite3
#modificar_tabla_paths()

db_path = 'Modeling_App.db'


def recreate_model_execution_table(database_path):
    try:
        # Conexión a la base de datos
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()

        # Desactivar las claves foráneas temporalmente
        cur.execute('''
        PRAGMA foreign_keys=OFF;
        ''')

        # Eliminar la tabla 'model_execution' si existe
        cur.execute('DROP TABLE IF EXISTS model_execution;')

        # Crear la tabla 'model_execution' desde cero, con la nueva columna 'version_id' y la clave foránea
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

        # Confirmar los cambios
        conn.commit()
        print("Tabla 'model_execution' recreada correctamente con la nueva estructura.")

    except sqlite3.Error as e:
        print(f"Error al recrear la tabla 'model_execution': {e}")
    finally:
        conn.close()

#recreate_model_execution_table('Modeling_App.db')

def modify_json_versions_table(db_path='Modeling_App.db'):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    try:
        # 1. Desactivar las claves foráneas temporalmente
        cur.execute("PRAGMA foreign_keys = OFF;")
        
        # 2. Renombrar la tabla antigua
        cur.execute("ALTER TABLE json_versions RENAME TO json_versions_old;")
        
        # 3. Crear la nueva tabla sin la columna project_id
        cur.execute('''
            CREATE TABLE json_versions (
                id_jsons INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_version TEXT NOT NULL,
                fecha_de_carga TEXT NOT NULL,
                version_id INTEGER,
                FOREIGN KEY (version_id) REFERENCES version(version_id)
            );
        ''')
        
        # 4. Copiar los datos de la tabla antigua a la nueva
        cur.execute('''
            INSERT INTO json_versions (id_jsons, nombre_version, fecha_de_carga, version_id)
            SELECT id_jsons, nombre_version, fecha_de_carga, version_id
            FROM json_versions_old;
        ''')
        
        # 5. Eliminar la tabla antigua
        cur.execute("DROP TABLE json_versions_old;")
        
        # 6. Reactivar las claves foráneas
        cur.execute("PRAGMA foreign_keys = ON;")
        
        conn.commit()
        print("Tabla json_versions modificada correctamente.")
    except sqlite3.Error as e:
        print(f"Error al modificar la tabla json_versions: {e}")
        conn.rollback()
    finally:
        conn.close()


#modify_json_versions_table()

def modificar_table(database_path):
    """
    Modifica la tabla 'name_files' para agregar la columna 'is_last_selected'.
    Si la columna ya existe, no realiza ninguna acción.

    :param database_path: Ruta al archivo de base de datos SQLite.
    """
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        
        # Verificar si la columna ya existe
        cursor.execute("PRAGMA table_info(project);")
        columns = [column[1] for column in cursor.fetchall()]
        
        if "is_last_selected" not in columns:
            # Agregar la columna 'is_last_selected'
            cursor.execute("ALTER TABLE project ADD COLUMN is_last_selected BOOLEAN DEFAULT 0;")
            print("Columna 'is_last_selected' agregada exitosamente.")
        else:
            print("La columna 'is_last_selected' ya existe. No se realizaron cambios.")
        
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error al modificar la tabla: {e}")
    finally:
        conn.close()

# Uso de la función
database_path = 'Modeling_App.db'
#modificar_table(database_path)
        
def restore_and_extend_model_execution(db_path):
    """
    Restaura la tabla 'model_execution' a partir de 'model_execution_backup_json',
    extendiendo la estructura con la columna 'json_version_id'.

    Args:
        db_path (str): Ruta a la base de datos SQLite.
    """
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        # Verificar si el respaldo existe
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='model_execution_backup_json';")
        backup_exists = cur.fetchone()

        if not backup_exists:
            print("El respaldo 'model_execution_backup_json' no existe. No se puede restaurar.")
            return

        # Eliminar la tabla 'model_execution' si existe para evitar conflictos
        cur.execute("DROP TABLE IF EXISTS model_execution;")

        # Crear la nueva tabla con la estructura extendida
        cur.execute('''
        CREATE TABLE model_execution (
            execution_id INTEGER PRIMARY KEY AUTOINCREMENT,
            version_id INTEGER,  -- Relación con la tabla 'versions'
            json_version_id INTEGER,  -- Relación con la tabla 'json_versions'
            execution_date TEXT,
            model_name TEXT,
            dataset_name TEXT,
            execution_state TEXT DEFAULT NULL,
            FOREIGN KEY (version_id) REFERENCES versions(version_id),
            FOREIGN KEY (json_version_id) REFERENCES json_versions(id_jsons)
        );
        ''')

        # Copiar los datos desde el respaldo a la nueva tabla
        cur.execute('''
        INSERT INTO model_execution (
            execution_id, version_id, json_version_id, execution_date, model_name, dataset_name, execution_state
        )
        SELECT execution_id, version_id, NULL, execution_date, model_name, dataset_name, execution_state
        FROM model_execution_backup_json;
        ''')

        # Confirmar los cambios
        conn.commit()
        print("Tabla 'model_execution' restaurada y extendida exitosamente.")

    except sqlite3.Error as e:
        print(f"Error al restaurar y extender la tabla 'model_execution': {e}")

    finally:
        if conn:
            conn.close()
# Reemplaza 'ruta_a_tu_base_de_datos.db' con la ruta a tu archivo SQLite

#restore_and_extend_model_execution(db_path)


def agregar_tabla(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Crear la tabla
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_configurations (
        user_id INTEGER PRIMARY KEY,
        valor_min_seg INTEGER NOT NULL,
        valor_max_seg INTEGER NOT NULL,
        num_select_filas INTEGER NOT NULL
    );
    """)
    conn.commit()
    print("Tabla 'user_configurations' creada exitosamente.")

    # Cerrar conexión
    conn.close()

def modificar_tabla(db_path):
    """
    Modifica la tabla user_configurations para incluir el campo value_dark_or_light.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Agregar la nueva columna si no existe
    cursor.execute("""
    ALTER TABLE user_configurations
    ADD COLUMN value_dark_or_light TEXT;
    """)
    conn.commit()
    print("Columna 'value_dark_or_light' agregada exitosamente.")
    conn.close()
    


def agregar_indice(db_path, table_name, index_name, column_name):
    """
    Agrega un índice a una tabla en SQLite.

    :param db_path: Ruta a la base de datos SQLite.
    :param table_name: Nombre de la tabla donde se agregará el índice.
    :param index_name: Nombre del índice a crear.
    :param column_name: Nombre de la columna que será indexada.
    """
    try:
        # Conexión a la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Verificar si el índice ya existe
        cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='index' AND name=?;
        """, (index_name,))
        exists = cursor.fetchone()

        if exists:
            print(f"El índice '{index_name}' ya existe en la tabla '{table_name}'.")
        else:
            # Crear el índice
            cursor.execute(f"""
            CREATE INDEX {index_name} 
            ON {table_name} ({column_name});
            """)
            conn.commit()
            print(f"Índice '{index_name}' creado exitosamente en la columna '{column_name}' de la tabla '{table_name}'.")
    except sqlite3.Error as e:
        print(f"Error al agregar el índice: {e}")
    finally:
        # Cerrar la conexión
        conn.close()
        


#agregar_indice(
    #db_path=db_path,
    #table_name="validation_scoring",
    #index_name="idx_version_id",
    #column_name="version_id"
#)




def crear_tabla_user_info(db_path):
    """
    Crea la tabla user_info en la base de datos SQLite con un índice único en hash_user_id.
    
    :param db_path: Ruta a la base de datos.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Crear la tabla
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_info (
            uuid TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
            hash_user_id VARCHAR(255) NOT NULL,
            nombre_user TEXT,
            mail_user TEXT,
            UNIQUE(hash_user_id) -- Índice único
        );
        """)
        conn.commit()
        print("Tabla 'user_info' creada exitosamente.")
    except sqlite3.Error as e:
        print(f"Error al crear la tabla: {e}")
    finally:
        conn.close()
        

#crear_tabla_user_info(db_path)


def mostrar_registros_user_info():
    conn = sqlite3.connect('Modeling_App.db')
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM user_info")
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except sqlite3.Error as e:
        print(f"Error al leer la tabla 'user_info': {e}")
    finally:
        conn.close()

# Mostrar registros
#mostrar_registros_user_info()

def modificar_tabla_user_info(db_path):
    """
    Modifica la tabla 'user_info' para que tenga una clave primaria INTEGER,
    elimine el campo 'uuid' y cree un índice único en 'hash_user_id'.

    :param db_path: Ruta a la base de datos SQLite.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Renombrar la tabla existente
        cursor.execute("ALTER TABLE user_configurations RENAME TO user_configurations_old;")

        # Crear la nueva tabla con la estructura actualizada
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_configurations (
            user_id INTEGER PRIMARY KEY, -- Clave primaria y referencia a user_info
            valor_min_seg INTEGER NOT NULL,
            valor_max_seg INTEGER NOT NULL,
            num_select_filas INTEGER NOT NULL,
            value_dark_or_light TEXT
            
            FOREIGN KEY (user_id) REFERENCES user_info(id)
                );
        """)

        # Migrar los datos necesarios de la tabla antigua
        cursor.execute("""
        INSERT INTO user_info (hash_user_id, mail_user)
        SELECT hash_user_id, mail_user FROM user_info_old;
        """)

        # Eliminar la tabla antigua
        cursor.execute("DROP TABLE user_info_old;")

        conn.commit()
        print("La tabla 'user_info' ha sido modificada exitosamente.")
    except sqlite3.Error as e:
        print(f"Error al modificar la tabla 'user_info': {e}")
    finally:
        conn.close()




def modificar_tabla_user_configurations(db_path):
    """
    Modifica la tabla 'user_configurations' para que haga referencia a 'user_info' por 'user_id'.
    También permite buscar dinámicamente por 'hash_user_id'.

    :param db_path: Ruta a la base de datos SQLite.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Renombrar la tabla existente
        cursor.execute("ALTER TABLE user_configurations RENAME TO user_configurations_old;")

        # Crear la nueva tabla con la estructura actualizada
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_configurations (
            user_id INTEGER PRIMARY KEY, -- Clave primaria y referencia a user_info
            valor_min_seg INTEGER NOT NULL,
            valor_max_seg INTEGER NOT NULL,
            num_select_filas INTEGER NOT NULL,
            value_dark_or_light TEXT, -- Columna adicional
            FOREIGN KEY (user_id) REFERENCES user_info(id)
        );
        """)

        # Migrar los datos necesarios de la tabla antigua
        cursor.execute("""
        INSERT INTO user_configurations (user_id, valor_min_seg, valor_max_seg, num_select_filas, value_dark_or_light)
        SELECT user_id, valor_min_seg, valor_max_seg, num_select_filas, value_dark_or_light FROM user_configurations_old;
        """)

        # Eliminar la tabla antigua
        cursor.execute("DROP TABLE user_configurations_old;")

        conn.commit()
        print("La tabla 'user_configurations' ha sido modificada exitosamente.")
    except sqlite3.Error as e:
        print(f"Error al modificar la tabla 'user_configurations': {e}")
    finally:
        conn.close()



def mostrar_registros_user_configurations(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM user_configurations")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except sqlite3.Error as e:
        print(f"Error al leer la tabla 'user_configurations': {e}")
    finally:
        conn.close()

# Mostrar los registros
#mostrar_registros_user_configurations(db_path)


import sqlite3

def verificar_claves_foraneas(db_path, table_name, claves_esperadas):
    """
    Verifica si las claves foráneas de una tabla hacen referencia a las columnas esperadas.

    :param db_path: Ruta a la base de datos SQLite.
    :param table_name: Nombre de la tabla a verificar.
    :param claves_esperadas: Lista de diccionarios con las claves esperadas. Cada diccionario debe incluir:
        - "column": Nombre de la columna en la tabla actual.
        - "referenced_table": Nombre de la tabla referenciada.
        - "referenced_column": Nombre de la columna referenciada.
    :return: True si todas las claves foráneas coinciden con las esperadas, False de lo contrario.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Obtener la lista de claves foráneas
        cursor.execute(f"PRAGMA foreign_key_list({table_name});")
        claves = cursor.fetchall()

        if not claves:
            print(f"La tabla '{table_name}' no tiene claves foráneas definidas o no existe.")
            return False

        # Convertir claves foráneas en un formato más fácil de manejar
        claves_actuales = []
        for clave in claves:
            claves_actuales.append({
                "column": clave[3],               # Columna en la tabla actual
                "referenced_table": clave[2],     # Tabla referenciada
                "referenced_column": clave[4]     # Columna referenciada
            })

        # Verificar si todas las claves esperadas están presentes
        claves_faltantes = [
            clave for clave in claves_esperadas
            if clave not in claves_actuales
        ]

        if claves_faltantes:
            print(f"Las siguientes claves foráneas faltan o no coinciden en la tabla '{table_name}':")
            for falta in claves_faltantes:
                print(f"Columna: {falta['column']}, Referencia: {falta['referenced_table']}({falta['referenced_column']})")
            return False

        print(f"Todas las claves foráneas esperadas están presentes en la tabla '{table_name}'.")
        return True

    except sqlite3.Error as e:
        print(f"Error al consultar las claves foráneas de la tabla '{table_name}': {e}")
        return False

    finally:
        conn.close()


db_path = "Modeling_App.db"  # Ruta a tu base de datos
table_name = "json_versions"  # Nombre de la tabla a verificar

# Claves foráneas esperadas
claves_esperadas = [
    {"column": "project_id", "referenced_table": "project", "referenced_column": "id"},
    {"column": "version_id", "referenced_table": "version", "referenced_column": "version_id"}
]

# Verificar las claves foráneas
resultado = verificar_claves_foraneas(db_path, table_name, claves_esperadas)

if resultado:
    print("Todas las claves foráneas están correctamente definidas.")
else:
    print("Algunas claves foráneas faltan o no coinciden.")