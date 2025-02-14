import sqlite3
from datetime import datetime

def comparar_ultimo_file_por_ejecucion(json_versiones_id, formato_fecha="%Y-%m-%d %H:%M:%S"):
    """
    Conecta a "Modeling_App.db" y, para un json_versiones_id dado, consulta las tablas
    validation_scoring y scoring, comparando el campo fecha_de_ejecucion para determinar
    cuál es el modelo más nuevo. Devuelve solo el id_nombre_file del registro con la fecha de
    ejecución más reciente.

    :param json_versiones_id: Valor de la versión de JSON a filtrar en ambas tablas.
    :param formato_fecha: Formato en el que se almacena la fecha (por defecto "%Y-%m-%d %H:%M:%S").
    :return: id_nombre_file del registro más reciente o None si no se encuentra.
    """
    conn = sqlite3.connect("Modeling_App.db")
    cursor = conn.cursor()

    # Consultar en validation_scoring para el json_versiones_id indicado
    query_vs = """
        SELECT id_nombre_file, fecha_de_ejecucion 
        FROM validation_scoring 
        WHERE json_versiones_id = ? 
        ORDER BY datetime(fecha_de_ejecucion) DESC 
        LIMIT 1
    """
    cursor.execute(query_vs, (json_versiones_id,))
    vs_registro = cursor.fetchone()

    # Consultar en scoring para el json_versiones_id indicado
    query_sc = """
        SELECT id_nombre_file, fecha_de_ejecucion 
        FROM scoring 
        WHERE json_versiones_id = ? 
        ORDER BY datetime(fecha_de_ejecucion) DESC 
        LIMIT 1
    """
    cursor.execute(query_sc, (json_versiones_id,))
    sc_registro = cursor.fetchone()

    selected_id = None

    if vs_registro and sc_registro:
        id_file_vs, fecha_vs = vs_registro
        id_file_sc, fecha_sc = sc_registro

        try:
            dt_vs = datetime.strptime(fecha_vs, formato_fecha)
            dt_sc = datetime.strptime(fecha_sc, formato_fecha)
        except Exception as e:
            print("Error al convertir fecha_de_ejecucion:", e)
            conn.close()
            return None

        if dt_vs >= dt_sc:
            selected_id = id_file_vs
        else:
            selected_id = id_file_sc

    elif vs_registro:
        selected_id = vs_registro[0]
    elif sc_registro:
        selected_id = sc_registro[0]
    else:
        print("No se encontraron registros para json_versiones_id:", json_versiones_id)
        conn.close()
        return None

    conn.close()

    print("El id del file correspondiente al modelo más nuevo es:", selected_id)
    return selected_id
