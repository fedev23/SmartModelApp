def obtener_opciones_versiones(versiones, id, name):
    """
    Función que devuelve un diccionario con todas las versiones para el selector.

    Args:
    - versiones (list): Lista de diccionarios con las versiones.
    - id (str): Clave para obtener el ID de cada versión.
    - name (str): Clave para obtener el nombre de cada versión.

    Returns:
    - dict: Diccionario con las opciones para el selector.
    """
    if versiones:
        return {str(version[id]): version[name] for version in versiones}
    else:
        return {"": "No hay versiones"}

def obtener_ultimo_id_version(versiones, id):
    """
    Función que devuelve el ID de la última versión.

    Args:
    - versiones (list): Lista de diccionarios con las versiones.
    - id (str): Clave para obtener el ID de cada versión.

    Returns:
    - str: El ID de la última versión como valor predeterminado.
    """
    if versiones:
        return str(versiones[-1][id])
    else:
        return ""
