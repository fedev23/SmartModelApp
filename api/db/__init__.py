# bd/__init__.py

# Especifica las funciones que quieres exportar
__all__ = ["get_user_projects", "add_project", "user_login", "execute_model", "eliminar_proyecto", "obtener_nombre_proyecto_por_id"]

# Importa las funciones desde funct_insert.py
from .fun_insert import get_user_projects, add_project, user_login, execute_model, eliminar_proyecto, obtener_nombre_proyecto_por_id
