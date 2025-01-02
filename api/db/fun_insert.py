import sqlite3
from datetime import datetime
import uuid

def add_project(user_id, name):
    conn = sqlite3.connect('Modeling_App.db')
    cur = conn.cursor()

    created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Insertar el nuevo proyecto en la tabla `project`
    cur.execute('''
    INSERT INTO project (user_id, name, created_date)
    VALUES (?, ?, ?)
    ''', (user_id, name, created_date))  # Ahora inserta 3 valores

    project_id = cur.lastrowid  # Obtener el ID del proyecto recién creado

    # Guardar el proyecto en `execution_log` para asociarlo al usuario
    cur.execute('''
    INSERT INTO execution_log (user_id, project_id, execution_date, model_name)
    VALUES (?, ?, ?, ?)
    ''', (user_id, project_id, created_date, name))

    conn.commit()
    conn.close()
    return project_id
# Función para obtener proyectos de un usuario específico
def eliminar_proyecto(project_id):
    conn = sqlite3.connect('Modeling_App.db')
    cur = conn.cursor()
    
    try:
        # Primero, eliminar registros en la tabla `file_name` relacionados con el proyecto (si existen)
        cur.execute('DELETE FROM name_files WHERE project_id = ?', (project_id,))

        # Eliminar las versiones asociadas al proyecto (si existen)
        cur.execute('DELETE FROM version WHERE project_id = ?', (project_id,))

        # Finalmente, eliminar el proyecto
        cur.execute('DELETE FROM project WHERE id = ?', (project_id,))
        
        conn.commit()
        print(f"Proyecto con ID {project_id} eliminado exitosamente.")
    except Exception as e:
        print(f"Error al eliminar el proyecto: {e}")
    finally:
        conn.close()
        
def get_user_projects(user_id):
    conn = sqlite3.connect('Modeling_App.db')
    cur = conn.cursor()

    # Realizar la consulta para obtener los proyectos del usuario específico
    cur.execute('''
    SELECT id, name, created_date
    FROM project
    WHERE user_id = ?
    ''', (user_id,))

    # Recuperar todos los resultados
    projects = cur.fetchall()
    conn.close()

    # Convertir los resultados en una lista de diccionarios
    return [{'id': project[0], 'name': project[1]} for project in projects]
# Función que gestiona el acceso del usuario

def user_login(user_id):
    projects = get_user_projects(user_id)
    
    if not projects:
        # Crear un proyecto nuevo si no existen proyectos para el usuario
        project_name = f"Proyecto de Usuario {user_id}"
        project_description = "Descripción del proyecto inicial"
        new_project_id = add_project(user_id, project_name, project_description)
        print(f"Nuevo proyecto creado con ID {new_project_id} para el usuario {user_id}.")
    else:
        # Mostrar los proyectos existentes del usuario
        print(f"Proyectos existentes para el usuario {user_id}:")
        for project in projects:
            print(f"- ID Proyecto: {project[0]}, Fecha Ejecución: {project[1]}, Modelo Ejecutado: {project[2]}")
            


def execute_model(user_id, project_id, model_name):
    conn = sqlite3.connect('Modeling_App.db')
    cur = conn.cursor()

    execution_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Insertar el registro de ejecución en `execution_log`
    cur.execute('''
    INSERT INTO execution_log (user_id, project_id, execution_date, model_name)
    VALUES (?, ?, ?, ?)
    ''', (user_id, project_id, execution_date, model_name))

    conn.commit()
    conn.close()




def  obtener_nombre_proyecto_por_id(proyecto_id):
    # Conectar a la base de datos (asegúrate de cambiar la ruta de la base de datos según sea necesario)
    conn = sqlite3.connect('Modeling_App.db')
    
    try:
        cursor = conn.cursor()
        
        # Consulta para obtener el nombre del proyecto por su ID
        cursor.execute("SELECT name FROM project WHERE id = ?", (proyecto_id,))
        
        # Obtener el resultado
        resultado = cursor.fetchone()
        
        # Verificar si se encontró el proyecto
        if resultado:
            return resultado[0]  # Devolver el nombre del proyecto
        else:
            return None  # Si no se encontró, retornar None

    except sqlite3.Error as e:
        print(f"Error al acceder a la base de datos: {e}  en obtener_nombre_proyecto_por_id")
        return None
    
    finally:
        # Cerrar la conexión
        conn.close()
        
        
def insert_table_model(user_id, project_id, execution_date, model_name, dataset_name, version_id, model_type, execution_state):
    try:
        # Conexión a la base de datos
        
        execution_id = str(uuid.uuid4())
        conn = sqlite3.connect('Modeling_App.db')
        cur = conn.cursor()

        # Insertar los datos en la tabla 'model_execution'
        cur.execute('''
        INSERT INTO model_execution (user_id, project_id, execution_date, model_name, dataset_name, version_id, execution_id, model_type, execution_state)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        ''', (user_id, project_id, execution_date, model_name, dataset_name, version_id, execution_id, model_type, execution_state))

        # Confirmar los cambios
        conn.commit()
        return f"Modelo '{model_name}' ejecutado  para el proyecto {project_id} con estado '{execution_state}'."

    except sqlite3.Error as e:
        print(f"Error al insertar datos en 'model_execution': {e}")
    finally:
        conn.close()


def show_execution_logs():
    conn = sqlite3.connect('Modeling_App.db')
    cur = conn.cursor()
    
    # Obtener todos los registros de execution_log
    cur.execute("SELECT * FROM execution_log;")
    logs = cur.fetchall()
    
    for log in logs:
        print(f"ID: {log[0]}, User ID: {log[1]}, Project ID: {log[2]}, Fecha de Ejecución: {log[3]}, Nombre del Modelo: {log[4]}")
    
    conn.close()

# Llama a esta función para ver los registros de ejecución
#show_execution_logs()

def get_latest_execution(project_id, model_name):
    conn = sqlite3.connect('Modeling_App.db')
    cur = conn.cursor()
    
    # Obtener el último registro de ejecución para el proyecto
    cur.execute('''
        SELECT execution_date, model_name, dataset_name
        FROM model_execution
        WHERE project_id = ? AND model_name = ?
        ORDER BY execution_date DESC
        LIMIT 1
    ''', (project_id, model_name))
    
    result = cur.fetchone()
    conn.close()
    
    # Retorna None si no hay resultados
    return result if result else (None, None, None)


def agregar_version(project_id, version_name):
    conn = sqlite3.connect('Modeling_App.db')
    cur = conn.cursor()

    # Obtener la fecha y hora actual
    execution_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Insertar la nueva versión en la tabla `version`
    cur.execute(''' 
    INSERT INTO version (project_id, nombre_version, execution_date)
    VALUES (?, ?, ?)
    ''', (project_id, version_name, execution_date))  # Solo 3 valores para 3 columnas

    # Obtener el ID de la versión recién creada
    version_id = cur.lastrowid  # Esto obtiene el ID de la versión recién insertada

    conn.commit()
    conn.close()
    
    return version_id  # Retornar el ID de la versión recién creada



def get_project_versions(project_id):
    conn = sqlite3.connect('Modeling_App.db')
    cur = conn.cursor()
    
    try:
        # Realizar la consulta para obtener las versiones del proyecto específico
        cur.execute('''
            SELECT version_id, nombre_version
            FROM version
            WHERE project_id = ?
        ''', (project_id,))
        
        # Recuperar todas las versiones
        versiones = cur.fetchall()
        
        # Convertir los resultaos en una lista de diccionarios
        files_list = [
            {
                'version_id': file[0],
                'nombre_version': file[1],
            }
            for file in versiones
        ]
        
        return files_list  # Retornar la lista de versiones
    
    except sqlite3.Error as e:
        print(f"Error al acceder a la base de datos: {e} en get_project_versions")
        return []
    
    finally:
        # Cerrar la conexión
        conn.close()
        



def obtener_nombre_version_por_id(version_id):
    # Conectar a la base de datos (asegúrate de cambiar la ruta de la base de datos según sea necesario)
    conn = sqlite3.connect('Modeling_App.db')
    
    try:
        cursor = conn.cursor()
        
        # Consulta para obtener el nombre del proyecto por su ID
        cursor.execute("SELECT nombre_version FROM version WHERE version_id = ?", (version_id,))
        
        # Obtener el resultado
        resultado = cursor.fetchone()
        
        # Verificar si se encontró el proyecto
        if resultado:
            return resultado[0]  # Devolver el nombre del proyecto
        else:
            return None  # Si no se encontró, retornar None

    except sqlite3.Error as e:
        print(f"Error al acceder a la base de datos: {e} en obtener_nombre_version_por_id")
        return None
    
    finally:
        # Cerrar la conexión
        conn.close()
        



def obtener_versiones_por_proyecto(columnas, tabla, condiciones=None, parametros=()):
    """
    Recupera datos de una tabla específica basada en columnas y condiciones opcionales.

    :param columnas: Lista de columnas a recuperar.
    :param tabla: Nombre de la tabla.
    :param condiciones: (Opcional) Cláusula WHERE para filtrar los datos.
    :param parametros: (Opcional) Parámetros para la cláusula WHERE.
    :return: Lista de diccionarios con los datos recuperados.
    """
    conn = sqlite3.connect('Modeling_App.db')
    cur = conn.cursor()

    try:
        # Crear la consulta de forma dinámica
        columnas_str = ", ".join(columnas)
        consulta = f"SELECT {columnas_str} FROM {tabla}"
        
        if condiciones:
            consulta += f" WHERE {condiciones}"
        
        # Ejecutar la consulta
        cur.execute(consulta, parametros)
        
        # Recuperar los datos
        datos = cur.fetchall()

        # Convertir los resultados en una lista de diccionarios
        datos_list = [
            {columnas[i]: dato for i, dato in enumerate(fila)}
            for fila in datos
        ]
        
        return datos_list

    except sqlite3.Error as e:
        print(f"Error al acceder a la base de datos: {e} en obtener_versiones_por_proyecto")
        return []
    
    finally:
        # Cerrar la conexión
        conn.close()
def insert_into_table(table_name, columns, values):
    """
    Inserta un registro en la tabla especificada y muestra el contenido actual de la tabla para depuración.
    
    :param table_name: Nombre de la tabla.
    :param columns: Lista de nombres de columnas.
    :param values: Lista de valores a insertar.
    :return: El ID del último registro insertado o None si hubo un error.
    """
    conn = sqlite3.connect('Modeling_App.db')
    cur = conn.cursor()
    
    try:
        # Construir la consulta de inserción
        placeholders = ', '.join(['?'] * len(values))
        columns_str = ', '.join(columns)
        query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
        
        # Ejecutar la inserción
        cur.execute(query, values)
        conn.commit()
        
        last_row_id = cur.lastrowid
        print(f"Registro insertado correctamente en '{table_name}' con ID: {last_row_id}")
        
        # Depuración: Mostrar los registros actuales de la tabla
        
        
        return last_row_id
    except sqlite3.IntegrityError as e:
        print(f"Error al insertar en '{table_name}': {e}")
        return None
    except sqlite3.Error as e:
        print(f"Error general al operar con '{table_name}': {e}")
        return None
    finally:
        conn.close()
        
def get_records(table, columns, join_clause=None, where_clause=None, where_params=()):
    """
    Recupera registros de una tabla específica en la base de datos fija.

    :param table: Nombre de la tabla de la que se desean recuperar los registros.
    :param columns: Lista de columnas a recuperar.
    :param join_clause: (Opcional) Cláusula JOIN para combinar tablas.
    :param where_clause: (Opcional) Condición WHERE para filtrar los registros.
    :param where_params: (Opcional) Parámetros para la cláusula WHERE.
    :return: Lista de diccionarios con los registros obtenidos.
    """
    database = 'Modeling_App.db'  # Base de datos fija
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    
    try:
        # Construir la consulta dinámica
        columns_str = ', '.join(columns)
        query = f"SELECT {columns_str} FROM {table}"
        
        if join_clause:
            query += f" {join_clause}"
        
        if where_clause:
            query += f" WHERE {where_clause}"
        
        cur.execute(query, where_params)
        
        # Recuperar los registros
        records = cur.fetchall()
        
        # Convertir los resultados en una lista de diccionarios
        records_list = [
            {columns[i]: record[i] for i in range(len(columns))}
            for record in records
        ]
        
        return records_list
    finally:
        # Asegurar el cierre de la conexión
        conn.close()


def delete_record(table_name, condition, condition_value):
    conn = sqlite3.connect('Modeling_App.db')
    cur = conn.cursor()

    query = f"DELETE FROM {table_name} WHERE {condition} = ?"
    cur.execute(query, (condition_value,))
    conn.commit()
    conn.close()
  
    
def obtener_valor_por_id(base_datos, tabla, columna_objetivo, columna_filtro, valor_filtro):
    """
    Obtiene el valor de una columna específica en una tabla, filtrando por un valor dado.

    Args:
        base_datos (str): Ruta a la base de datos SQLite.
        tabla (str): Nombre de la tabla donde se realizará la consulta.
        columna_objetivo (str): Nombre de la columna cuyo valor se desea obtener.
        columna_filtro (str): Nombre de la columna utilizada para el filtro.
        valor_filtro: Valor para filtrar la consulta.

    Returns:
        El valor encontrado o None si no se encuentra.
    """
    conn = sqlite3.connect(base_datos)
    
    try:
        cursor = conn.cursor()
        
        # Construcción dinámica de la consulta
        query = f"""
        SELECT {columna_objetivo} 
        FROM {tabla} 
        WHERE {columna_filtro} = ?
        """
        cursor.execute(query, (valor_filtro,))
        
        # Obtener el resultado
        resultado = cursor.fetchone()
        
        # Verificar si se encontró un valor
        if resultado:
            return resultado[0]  # Devolver el valor encontrado
        else:
            return None  # Si no se encontró, retornar None

    except sqlite3.Error as e:
        print(f"Error al acceder a la base de datos: {e} obtener_valor_por_id")
        return None

    finally:
        # Cerrar la conexión
        conn.close()
        
        
def eliminar_version(nombre_tabla, nombre_columna_id, id_dato):
    # Conexión a la base de datos
    conn = sqlite3.connect('Modeling_App.db')
    cur = conn.cursor()

    try:
        # Validar que el nombre de la tabla y la columna sean identificadores válidos
        if not nombre_tabla.isidentifier() or not nombre_columna_id.isidentifier():
            raise ValueError("Nombre de tabla o columna no válido")

        # Crear la consulta SQL de forma segura
        query = f"DELETE FROM {nombre_tabla} WHERE {nombre_columna_id} = ?"
        cur.execute(query, (id_dato,))
        
        # Confirmar los cambios
        conn.commit()
        print(f"Dato con ID {id_dato} eliminado exitosamente de la tabla {nombre_tabla}.")
    except Exception as e:
        print(f"Error al eliminar el dato: {e}")
    finally:
        # Cerrar la conexión
        conn.close()
   
def add_param_versions(project_id, version_id, name):
    conn = sqlite3.connect('Modeling_App.db')
    cur = conn.cursor()

    # Obtener la fecha de carga actual
    fecha_de_carga = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Insertar una nueva versión de parámetros en la tabla json_versions
    cur.execute('''
    INSERT INTO json_versions (nombre_version, fecha_de_carga, project_id, version_id)
    VALUES (?, ?, ?, ?)
    ''', (name, fecha_de_carga, project_id, version_id))  # Se insertan los valores para nombre, fecha, project_id y version_id

    # Obtener el ID de la nueva versión de parámetros insertada
    version_param_id = cur.lastrowid

    # Confirmar los cambios en la base de datos
    conn.commit()

    # Cerrar la conexión
    conn.close()

    return version_param_id

def   get_project_versions_param(project_id, version_id):
    conn = sqlite3.connect('Modeling_App.db')
    cur = conn.cursor()
    
    try:
        # Realizar la consulta para obtener las versiones específicas
        cur.execute('''
            SELECT j.id_jsons, j.nombre_version
            FROM json_versions j
            JOIN version v ON j.version_id = v.version_id
            WHERE v.project_id = ? AND j.version_id = ?
        ''', (project_id, version_id))
        
        # Recuperar los resultados
        versiones = cur.fetchall()
        
        # Convertir los resultados en una lista de diccionarios
        files_list = [
            {
                'id_jsons': file[0],
                'nombre_version': file[1],
            }
            for file in versiones
        ]
        
        return files_list  # Retornar la lista de resultados
    
    except sqlite3.Error as e:
        print(f"Error al acceder a la base de datos: {e}")
        return []
    
    finally:
        # Cerrar la conexión
        conn.close()          

def get_project_versions_param_mejorada(project_id, version_id=None):
    """
    Obtiene las versiones de parámetros asociadas a un proyecto específico.
    Permite filtrar por una versión específica dentro del proyecto.

    :param project_id: ID del proyecto asociado.
    :param version_id: ID específico de la versión (opcional).
    :return: Lista de diccionarios con las versiones de parámetros y sus nombres.
    """
    conn = sqlite3.connect('Modeling_App.db')
    cur = conn.cursor()
    
    try:
        # Consulta base
        query = '''
            SELECT j.id_jsons, j.nombre_version, j.version_id
            FROM json_versions j
            INNER JOIN version v ON j.version_id = v.version_id
            WHERE v.project_id = ?
        '''
        params = [project_id]
        
        # Filtro adicional por version_id
        if version_id:
            query += " AND j.version_id = ?"
            params.append(version_id)
        
        # Ejecutar la consulta
        cur.execute(query, params)
        
        # Recuperar los resultados
        versiones = cur.fetchall()
        
        # Convertir resultados en lista de diccionarios
        files_list = [
            {
                'id_jsons': row[0],
                'nombre_version': row[1],
                'version_id': row[2]
            }
            for row in versiones
        ]
        
        return files_list
    
    except sqlite3.Error as e:
        print(f"Error al acceder a la base de datos: {e}")
        return []
    
    finally:
        conn.close()
               
def obtener_valor_por_id_versiones(id_files , base_datos='Modeling_App.db'):
    
        conn = sqlite3.connect(base_datos)
        
        try:
            cursor = conn.cursor()
            
            # Consulta para obtener el nombre del archivo por project_id
            query = """
            SELECT nombre_version 
            FROM json_versions 
            WHERE id_jsons  = ?
            """
            cursor.execute(query, (id_files ,))
            
            # Obtener el resultado
            resultado = cursor.fetchone()
            
            # Verificar si se encontró un archivo
            if resultado:
                return resultado[0]  # Devolver el nombre del archivo
            else:
                return None  # Si no se encontró, retornar None

        except sqlite3.Error as e:
            print(f"Error al acceder a la base de datos: {e}, en obtener_valor_por_id_versiones")
            return None

        finally:
            # Cerrar la conexión
            conn.close()

def obtener_path_por_proyecto_version(version_id, tipo_path):
    """
    Obtiene el path asociado a una versión específica y un tipo de path.

    :param version_id: ID de la versión.
    :param tipo_path: Tipo de path (e.g., 'entrada', 'salida').
    :return: Path asociado o None si no se encuentra.
    """
    conn = sqlite3.connect('Modeling_App.db')
    cur = conn.cursor()
    try:
        # Consulta para obtener el path basado en version_id y tipo_path
        consulta = '''
            SELECT path
            FROM paths_de_ejecucion
            WHERE version_id = ? AND tipo_path = ?
        '''
        cur.execute(consulta, (version_id, tipo_path))
        datos = cur.fetchone()

        return datos[0] if datos else None

    except sqlite3.Error as e:
        print(f"Error al acceder a la base de datos: {e} error en obtener_path_por_version")
        return None

    finally:
        conn.close()
        
                
def insertar_path(path, version_id, tipo_path):
    """
    Inserta un registro en la tabla paths_de_ejecucion.

    :param path: Ruta a insertar.
    :param version_id: ID de la versión asociada.
    :param tipo_path: Tipo de path (entrada, salida, etc.).
    """
    conn = sqlite3.connect('Modeling_App.db')
    cur = conn.cursor()
    try:
        cur.execute('''
            INSERT INTO paths_de_ejecucion (path, version_id, tipo_path)
            VALUES (?, ?, ?)
        ''', (path, version_id, tipo_path))
        conn.commit()
        print("Path insertado correctamente con tipo_path:", tipo_path)
    except sqlite3.IntegrityError as e:
        print(f"Error al insertar el path: {e}")
    finally:
        conn.close()


def insert_record(database_path, table, columns, values):
    """
    Inserta un registro en una tabla específica de una base de datos SQLite.

    :param database_path: Ruta al archivo de la base de datos SQLite.
    :param table: Nombre de la tabla donde se insertará el registro.
    :param columns: Lista de nombres de las columnas en las que se insertarán los valores.
    :param values: Lista de valores a insertar. El orden debe coincidir con las columnas.
    :return: None
    """
    try:
        # Conexión a la base de datos
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()
        
        # Construir la consulta de inserción
        columns_str = ', '.join(columns)
        placeholders = ', '.join(['?' for _ in values])
        query = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"
        
        # Ejecutar la consulta
        cur.execute(query, values)
        
        # Confirmar los cambios
        conn.commit()
        print(f"Registro insertado correctamente en la tabla '{table}'.")

    except sqlite3.Error as e:
        print(f"Error al insertar registro en la tabla '{table}': {e}")
    finally:
        conn.close()