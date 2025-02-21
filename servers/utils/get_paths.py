

import os

def get_output_path(nombre_file: str, global_session, global_session_V2, modo: str = "full") -> str:
    """
    Construye y retorna la ruta de salida utilizando las variables de sesión global,
    de acuerdo al modo especificado.

    Parámetros:
        nombre_file (str): Nombre del archivo, del cual se extraerá su basename (para el modo "full" o "scoring").
        global_session: Objeto que provee métodos para obtener datos de la sesión.
        global_session_V2: Objeto que provee atributos/métodos adicionales de la sesión.
        modo (str): Modo de construcción del path. Puede ser:
            - "desarrollo": Retorna el path sin parámetros de versión y sin nombre de archivo.
            - "in sample": Retorna el path con parámetros de versión, sin incluir el nombre de archivo.
            - "full" o "scoring": Retorna el path completo, incluyendo la subcarpeta del nombre_file y su basename.

    Retorna:
        str: Ruta de salida construida.
    """
    base_path = (
        f"/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/"
        f"datos_salida_{global_session.get_id_user()}/"
        f"proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/"
        f"version_{global_session.get_id_version()}_{global_session.get_versiones_name()}"
    )
    
    if modo == "desarrollo":
        # Path sin parámetros de versión ni nombre de archivo
        salida = f"{base_path}/Reportes"
    elif modo == "in_sample":
        # Path con parámetros de versión (version_parametros) y sin nombre de archivo
        salida = (
            f"{base_path}/version_parametros_{global_session.get_version_parametros_id()}_{global_session.get_versiones_parametros_nombre()}/Reportes"
        )
    elif modo in ("full", "scoring"):
        # Path completo con parámetros de versión, subcarpeta adicional y basename del archivo
        salida = (
            f"{base_path}/version_parametros_{global_session.get_version_parametros_id()}_{global_session.get_versiones_parametros_nombre()}/"
            f"{global_session_V2.nombre_file_sin_extension_validacion_scoring.get()}/Reportes"
        )
    else:
        raise ValueError("Modo no reconocido. Utilice 'desarrollo', 'in sample', 'full' o 'scoring'.")
    
    return salida

