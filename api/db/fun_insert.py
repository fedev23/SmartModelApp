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
