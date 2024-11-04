import sqlite3
from datetime import datetime

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
    return [{'id': project[0], 'name': project[1], 'created_date': project[2]} for project in projects]
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




def obtener_nombre_proyecto_por_id(proyecto_id):
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
        print(f"Error al acceder a la base de datos: {e}")
        return None
    
    finally:
        # Cerrar la conexión
        conn.close()
        
        
def insert_table_model(user_id, project_id, model_name, dataset_name):
    conn = sqlite3.connect('Modeling_App.db')
    cur = conn.cursor()

    # Obtener la fecha y hora de ejecución
    execution_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Insertar el registro en `model_execution`
    cur.execute('''
        INSERT INTO model_execution (user_id, project_id, execution_date, model_name, dataset_name)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, project_id, execution_date, model_name, dataset_name))

    conn.commit()
    conn.close()
    print(f"Ejecución registrada en 'model_execution': {model_name} para el proyecto ID {project_id} a las {execution_date}.")



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