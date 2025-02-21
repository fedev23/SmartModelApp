from api.db.sqlite_utils import *
from clases.global_session import *
from clases.global_sessionV3 import *

def manejo_de_ultimo_seleccionado(
    is_initializing,
    input_select_value,
    ultimo_id_func,
    global_set_func,
    actualizar_ultimo_func,
    obtener_ultimo_func,
    obtener_opciones_func,
    mapear_clave_func,
    ui_update_func,
    input_select_name,
    db_table,
    db_column_id,
    db_column_name
):
    
    if is_initializing():
        print(f"⚡ Inicialización detectada para {input_select_name}")
        is_initializing.set(False)  # Marcar como inicializado

        # Obtener el último ID almacenado
        ultimo_id = ultimo_id_func()
        print(f"📌 Último ID almacenado obtenido: {ultimo_id}")

        if ultimo_id:
            print(f"✅ Último ID existente: {ultimo_id}, actualizando global...")
            global_set_func(ultimo_id)

            # Obtener el último valor almacenado en la DB
            ultimo_select = obtener_ultimo_func(db_table, db_column_name)
            print(f"📌 Último valor obtenido desde la BD: {ultimo_select}")

            # Obtener opciones disponibles y mapear clave
            opciones = obtener_opciones_func()
            print(f"📌 Opciones obtenidas: {opciones}")

            key_match = mapear_clave_func(ultimo_select, opciones)
            print(f"🔎 Clave mapeada en opciones: {key_match}")

            # Actualizar selector en la UI
            selected_value = key_match if key_match else next(iter(ultimo_select), "")
            print(f"📌 Valor seleccionado para la UI: {selected_value}")

            ui_update_func(input_select_name, choices=opciones, selected=selected_value)
        
        else:
            print(f"⚠️ No hay último ID, usando input_select_value: {input_select_value}")
            global_set_func(input_select_value)
            actualizar_ultimo_func(db_table, db_column_id, input_select_value)

        return

    # Lógica para cambios explícitos en el selector
    print(f"📌 Revisando cambios explícitos en selector...")
    ultimo_id = ultimo_id_func()
    print(f"📌 Último ID después de la inicialización: {ultimo_id}")

    if ultimo_id:
        if ultimo_id != input_select_value:
            print(f"⚡ Cambio detectado: {ultimo_id} -> {input_select_value}")
            global_set_func(input_select_value)
            actualizar_ultimo_func(db_table, db_column_id, input_select_value)
        else:
            print(f"✅ No hay cambios en el selector, mantiene: {ultimo_id}")
    else:
        print(f"⚠️ No hay último ID, actualizando con input_select_value: {input_select_value}")
        global_set_func(input_select_value)
        actualizar_ultimo_func(db_table, db_column_id, input_select_value)

def manejo_de_ultimo_seleccionado_niveles_ScoreCards(
    is_initializing,
    input_select_value,
    ultimo_id_func,
    global_name_func,
    global_set_func,
    actualizar_ultimo_func,
    obtener_ultimo_func,
    obtener_opciones_func,
    mapear_clave_func,
    ui_update_func,
    input_select_name,
    db_table,
    db_column_id,
    db_column_name,
    db
):
    
    if is_initializing():
        print(f"⚡ Inicialización detectada para {input_select_name}")
        is_initializing.set(False)  # Marcar como inicializado

        # Obtener el último ID almacenado
        ultimo_id = ultimo_id_func()
        print(ultimo_id, "ultimo_id??")
        if ultimo_id:
            global_set_func(ultimo_id)

            # Obtener el último valor almacenado en la DB
            ultimo_select = obtener_ultimo_func(db_table, db_column_name)
            print(f"utlimo seleccionado? {ultimo_select}")
            # Obtener opciones disponibles y mapear clave
            opciones = obtener_opciones_func()
            
            key_match = mapear_clave_func(ultimo_select, opciones)
            
            if key_match is None:
                ultimo_bd = obtener_ultimo_id_json_por_version(db, db_table, db_column_id, global_session.get_id_version()) 
                nombre_version = obtener_nombre_version_por_id_json(db, db_table, ultimo_bd)
                #global_name_func(nombre_version)
                
                key_match = mapear_clave_func(nombre_version, opciones)
                
            # Actualizar selector en la UI
            selected_value = key_match if key_match else next(iter(ultimo_select), "")
            
            ui_update_func(input_select_name, choices=opciones, selected=selected_value)
        
        else:
            global_name_func(None)
            global_set_func(input_select_value)
            actualizar_ultimo_func(db_table, db_column_id, input_select_value)

        return

    # Lógica para cambios explícitos en el selector
    print(f"📌 Revisando cambios explícitos en selector...")
    ultimo_id = ultimo_id_func()
    print(f"📌 Último ID después de la inicialización: {ultimo_id}")

    if ultimo_id:
        if ultimo_id != input_select_value:
            print(f"⚡ Cambio detectado: {ultimo_id} -> {input_select_value}")
            global_set_func(input_select_value)
            actualizar_ultimo_func(db_table, db_column_id, input_select_value)
        else:
            print(f"✅ No hay cambios en el selector, mantiene: {ultimo_id}")
    else:
        print(f"⚠️ No hay último ID, actualizando con input_select_value: {input_select_value}")
        global_set_func(input_select_value)
        actualizar_ultimo_func(db_table, db_column_id, input_select_value)




def generar_paths_insa(global_session):
    """
    Genera los paths de entrada y salida basados en los valores de `global_session`.

    :param global_session: Objeto con métodos `get_id_user()`, `get_id_proyecto()`, etc.
    :return: Tupla con (path_datos_entrada, path_datos_salida)
    """
    base_path = "/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat"

    user_id = global_session.get_id_user()
    proyecto_id = global_session.get_id_proyecto()
    proyecto_nombre = global_session.get_name_proyecto()
    version_id = global_session.get_id_version()
    version_nombre = global_session.get_versiones_name()
    param_id = global_session.get_version_parametros_id()
    param_nombre = global_session.get_versiones_parametros_nombre()

    # Construcción de paths
    path_datos_entrada = (
        f"{base_path}/datos_entrada_{user_id}/proyecto_{proyecto_id}_{proyecto_nombre}/"
        f"version_{version_id}_{version_nombre}/version_parametros_{param_id}_{param_nombre}"
    )

    path_datos_salida = (
        f"{base_path}/datos_salida_{user_id}/proyecto_{proyecto_id}_{proyecto_nombre}/"
        f"version_{version_id}_{version_nombre}/version_parametros_{param_id}_{param_nombre}"
    )

    return path_datos_entrada, path_datos_salida



def generar_paths_of_sample_y_scoring(global_session, global_session_V2, tipo='entrada'):
    """
    Genera el path para 'datos_entrada' o 'datos_salida' según la sesión actual.

    Args:
        global_session: Objeto que contiene la información de la sesión.
        global_session_V2: Objeto que contiene información adicional de la sesión.
        tipo (str): 'entrada' para datos de entrada, 'salida' para datos de salida.

    Returns:
        str: El path generado según el tipo solicitado.
    """
    tipo_path = 'datos_entrada' if tipo == 'entrada' else 'datos_salida'
    
    path = (
        f"/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/"
        f"{tipo_path}_{global_session.get_id_user()}/"
        f"proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/"
        f"version_{global_session.get_id_version()}_{global_session.get_versiones_name()}/"
        f"version_parametros_{global_session.get_version_parametros_id()}_{global_session.get_versiones_parametros_nombre()}/"
        f"{global_session_V2.nombre_file_sin_extension_validacion_scoring.get()}"
    )
    
    return path