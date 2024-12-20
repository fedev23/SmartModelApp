# bd/__init__.py

# Especifica las funciones que quieres exportar
__all__ = ["get_user_projects", "add_project", "user_login", "execute_model", "eliminar_proyecto", "obtener_nombre_proyecto_por_id", "insert_table_model", "get_latest_execution", "agregar_version",
           "get_project_versions", "obtener_nombre_version_por_id", "eliminar_version", "eliminar_version", "obtener_versiones_por_proyecto", "insert_into_table", "get_records", "obtener_valor_por_id", "add_param_versions", "get_project_versions_param", "obtener_valor_por_id_versiones", "obtener_path_por_proyecto_version", "insertar_path"]

# Importa las funciones desde funct_insert.py
from .fun_insert import get_user_projects, add_project, user_login, execute_model, eliminar_proyecto, obtener_nombre_proyecto_por_id, insert_table_model, get_latest_execution, agregar_version,get_project_versions, obtener_nombre_version_por_id , eliminar_version, obtener_versiones_por_proyecto, insert_into_table, get_records, obtener_valor_por_id, add_param_versions, get_project_versions_param,obtener_valor_por_id_versiones, obtener_path_por_proyecto_version, insertar_path
