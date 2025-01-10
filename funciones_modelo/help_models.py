from api.db.sqlite_utils import *
from api.db import *

def obtener_estado_por_modelo(modelo, nombre_modelo):
    """
    Busca un modelo por su nombre y retorna su estado de ejecución.

    Args:
        modelo (dict): Diccionario que contiene información del modelo.
        nombre_modelo (str): Nombre del modelo a buscar.

    Returns:
        str: Estado de ejecución si se encuentra el modelo.
        str: Mensaje de error si no se encuentra el modelo.
    """
    if modelo.get('model_name') == nombre_modelo:
        return modelo.get('execution_state', 'No disponible')

    return f""

def obtener_fecha_por_modelo(modelo, nombre_modelo):
    """
    Busca un modelo por su nombre y retorna su fecha de ejecución.

    Args:
        modelo (dict): Diccionario que contiene información del modelo.
        nombre_modelo (str): Nombre del modelo a buscar.

    Returns:
        str: Fecha de ejecución si se encuentra el modelo.
        str: Mensaje de error si no se encuentra el modelo.
    """
    if modelo.get('model_name') == nombre_modelo:
        return modelo.get('execution_date', 'No disponible')

    return f""





def procesar_etapa(base_datos, id_version, etapa_nombre):
    """
    Procesa una etapa específica, obteniendo estado y fecha para el modelo.

    :param base_datos: Ruta a la base de datos.
    :param id_version: ID de la versión actual.
    :param etapa_nombre: Nombre de la etapa a procesar.
    :return: Tupla con (estado_model, fecha_model).
    """
    # Obtener el último modelo
    ult_model = obtener_ultimo_modelo_por_version_y_nombre(base_datos, id_version, etapa_nombre)

    # Obtener el estado del modelo para la etapa
    estado_model = obtener_estado_por_modelo(ult_model, etapa_nombre)
   
    # Obtener la fecha del modelo para la etapa
    fecha_model = obtener_fecha_por_modelo(ult_model, etapa_nombre)
    

    # Retornar el estado y la fecha como una tupla
    return estado_model, fecha_model




def agregar_datos_model_execution(version_id, name, nombre_dataset, estado, json_version_id=None):
    """
    Inserta un registro en la tabla model_execution con los datos proporcionados.

    :param version_id: ID de la versión actual.
    :param name: Nombre del modelo.
    :param nombre_dataset: Nombre del dataset.
    :param estado: Estado de la ejecución (por ejemplo, 'Exito', 'Error', etc.).
    :param json_version_id: (Opcional) ID del JSON de la versión, si aplica.
    :return: ID del último registro insertado (add).
    """
    # Valores requeridos para la inserción
    version_id = version_id
    nombre_modelo = name
    dataset_name = nombre_dataset
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    execution_state = estado  # Puedes cambiarlo según corresponda

    # Definir la tabla y las columnas
    table_name = "model_execution"
    columns = ['version_id', 'execution_date', 'model_name', 'dataset_name', 'execution_state']
    values = [version_id, current_timestamp, nombre_modelo, dataset_name, execution_state]

    # Agregar json_version_id si se proporciona
    if json_version_id is not None:
        columns.append('json_version_id')
        values.append(json_version_id)

    # Llamar a la función de inserción
    add = insert_into_table(table_name, columns, values)

    # Retornar el ID del registro insertado
    return add


def agregar_datos_model_execution_por_json_version(json_version_id, name, nombre_dataset, estado):
    """
    Inserta un registro en la tabla model_execution basado únicamente en json_version_id.

    :param json_version_id: ID del JSON de la versión.
    :param name: Nombre del modelo.
    :param nombre_dataset: Nombre del dataset.
    :param estado: Estado de la ejecución (por ejemplo, 'Exito', 'Error', etc.).
    :return: ID del último registro insertado.
    """
    # Valores requeridos para la inserción
    nombre_modelo = name
    dataset_name = nombre_dataset
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    execution_state = estado

    # Definir la tabla y las columnas
    table_name = "model_execution"
    columns = ['json_version_id', 'execution_date', 'model_name', 'dataset_name', 'execution_state']
    values = [json_version_id, current_timestamp, nombre_modelo, dataset_name, execution_state]

    # Llamar a la función de inserción
    add = insert_into_table(table_name, columns, values)

    # Retornar el ID del registro insertado
    return add



def procesar_etapa_in_sample_2(base_datos, json_version_id, etapa_nombre):
    """
    Procesa una etapa específica, obteniendo estado y fecha para el modelo.

    :param base_datos: Ruta a la base de datos.
    :param id_version: ID de la versión actual.
    :param etapa_nombre: Nombre de la etapa a procesar.
    :return: Tupla con (estado_model, fecha_model).
    """
    # Obtener el último modelo
    ult_model = obtener_ultimo_modelo_por_version_json(base_datos, json_version_id)
    
    # Obtener el estado del modelo para la etapa
    estado_model = obtener_estado_por_modelo(ult_model, etapa_nombre)
    
    # Obtener la fecha del modelo para la etapa
    fecha_model = obtener_fecha_por_modelo(ult_model, etapa_nombre)
    
    # Retornar el estado y la fecha como una tupla
    return estado_model, fecha_model


def procesar_etapa_in_sample(base_datos, json_version_id, etapa_nombre):
    """
    Procesa una etapa específica para in_sample, obteniendo estado y fecha del modelo.

    :param base_datos: Ruta a la base de datos.
    :param json_version_id: ID de la versión JSON en la tabla json_versions.
    :param etapa_nombre: Nombre de la etapa a procesar.
    :return: Tupla con (estado_model, fecha_model).
    """
    try:
        conn = sqlite3.connect(base_datos)
        cur = conn.cursor()

        # Obtener el último modelo relacionado únicamente con json_version_id
        cur.execute('''
        SELECT me.model_name, me.execution_state, me.execution_date
        FROM model_execution me
        WHERE me.json_version_id = ?
        ORDER BY datetime(me.execution_date) DESC
        LIMIT 1;
        ''', (json_version_id,))

        result = cur.fetchone()

        if result:
            model_name, estado_model, fecha_model = result
            #print(f"Modelo encontrado: {model_name}, Estado: {estado_model}, Fecha: {fecha_model}")
            return estado_model, fecha_model
        else:
            print(f"No se encontró ningún modelo para json_version_id={json_version_id} en etapa '{etapa_nombre}'.")
            return "", ""

    except sqlite3.Error as e:
        print(f"Error al procesar etapa in_sample para json_version_id={json_version_id}: {e}")
        return "", ""

    finally:
        if conn:
            conn.close()



def agregar_datos_model_execution_in_sample(base_datos, version_id, json_version_id, name, nombre_dataset, estado):
    """
    Inserta un registro en la tabla model_execution para in_sample.

    :param base_datos: Ruta a la base de datos.
    :param version_id: ID de la versión principal en la tabla version.
    :param json_version_id: ID de la versión JSON en la tabla json_versions.
    :param name: Nombre del modelo.
    :param nombre_dataset: Nombre del dataset.
    :param estado: Estado de la ejecución (por ejemplo, 'Exito', 'Error', etc.).
    :return: ID del último registro insertado (add).
    """
    from datetime import datetime

    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(base_datos)
    cur = conn.cursor()

    try:
        # Insertar el nuevo registro
        cur.execute('''
        INSERT INTO model_execution (
            version_id, json_version_id, execution_date, model_name, dataset_name, execution_state
        )
        VALUES (?, ?, ?, ?, ?, ?);
        ''', (version_id, json_version_id, current_timestamp, name, nombre_dataset, estado))

        conn.commit()
        add = cur.lastrowid
        #print(f"Registro agregado exitosamente con ID: {add}")
        return add

    except sqlite3.Error as e:
        print(f"Error al insertar datos en in_sample: {e}")
        return None

    finally:
        if conn:
            conn.close()


def check_execution_status(db_path, version_id=None, json_id=None):
    print(f"Valores recibidos - version_id={version_id}, json_id={json_id}")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        if version_id:
            print(f"Consultando por version_id={version_id}")
            cursor.execute("""
            SELECT execution_state 
            FROM model_execution 
            WHERE version_id = ?;
            """, (version_id,))
        elif json_id:
            print(f"Consultando por json_id={json_id}")
            cursor.execute("""
            SELECT execution_state 
            FROM model_execution 
            WHERE json_version_id = ?;
            """, (json_id,))
        else:
            print("Error: No se proporcionaron version_id ni json_id.")
            return None

        result = cursor.fetchone()
        print(f"Resultado de la consulta: {result}")
        return result[0] if result else None
    except sqlite3.Error as e:
        print(f"Error al consultar la base de datos: {e}")
        return None
    finally:
        conn.close()
