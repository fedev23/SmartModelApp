from api.db.sqlite_utils import *
from api.db import *
from api.db.utils.update_genric import *
import os , re


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


def obtener_fecha_por_modelo_Score(modelo, nombre_modelo):
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
        return modelo.get('fecha_de_ejecucion', 'No disponible')

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




def procesar_etapa_validacion_full(base_datos, id_validacion_sc, etapa_nombre):
    """
    Procesa una etapa específica, obteniendo estado y fecha para el modelo.

    :param base_datos: Ruta a la base de datos.
    :param id_version: ID de la versión actual.
    :param etapa_nombre: Nombre de la etapa a procesar.
    :return: Tupla con (estado_model, fecha_model).
    """
    # Obtener el último modelo
    nombre_modelo = etapa_nombre
    ult_model = obtener_ultimo_modelo_por_validacion_sc_y_nombre(base_datos, id_validacion_sc, nombre_modelo)

    print(f"ult_model {ult_model}")
    # Obtener el estado del modelo para la etapa
    estado_model = obtener_estado_por_modelo(ult_model, etapa_nombre)
   
    print(f"estado_model {estado_model}")
    # Obtener la fecha del modelo para la etapa
    fecha_model = obtener_fecha_por_modelo(ult_model, etapa_nombre)
    
    print(f"fecha_model {fecha_model}")

    # Retornar el estado y la fecha como una tupla
    return estado_model, fecha_model


def procesar_etapa_validacion_scroing(base_datos, id_score, etapa_nombre):
    """
    Procesa una etapa específica, obteniendo estado y fecha para el modelo.

    :param base_datos: Ruta a la base de datos.
    :param id_version: ID de la versión actual.
    :param etapa_nombre: Nombre de la etapa a procesar.
    :return: Tupla con (estado_model, fecha_model).
    """
    # Obtener el último modelo
    nombre_modelo = etapa_nombre
    ult_model = obtener_ultimo_scoring_por_json_version_y_modelo(base_datos, id_score, nombre_modelo)

    print(f"ult_model {ult_model}")
    # Obtener el estado del modelo para la etapa
    estado_model = obtener_estado_por_modelo(ult_model, etapa_nombre)
   
    print(f"estado_model {estado_model}")
    # Obtener la fecha del modelo para la etapa
    fecha_model = obtener_fecha_por_modelo_Score(ult_model, etapa_nombre)
    
    print(f"fecha_model {fecha_model}")

    # Retornar el estado y la fecha como una tupla
    return estado_model, fecha_model


from datetime import datetime

def agregar_datos_model_execution(version_id, name, nombre_dataset, estado, json_version_id=None, mensaje_error=None, dataset_id=None):
    """
    Inserta un registro en la tabla model_execution con los datos proporcionados.

    :param version_id: ID de la versión actual.
    :param name: Nombre del modelo.
    :param nombre_dataset: Nombre del dataset.
    :param estado: Estado de la ejecución (por ejemplo, 'Exito', 'Error', etc.).
    :param json_version_id: (Opcional) ID del JSON de la versión, si aplica.
    :param mensaje_error: (Opcional) Mensaje de error, si aplica.
    :param dataset_id: (Opcional) ID del dataset relacionado.
    :return: ID del último registro insertado (add).
    """
    # Valores requeridos para la inserción
    version_id = version_id
    nombre_modelo = name
    dataset_name = nombre_dataset
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    execution_state = estado  # Puedes cambiarlo según corresponda
    mensaje_error = mensaje_error

    # Definir la tabla y las columnas
    table_name = "model_execution"
    columns = ['version_id', 'execution_date', 'model_name', 'dataset_name', 'execution_state', 'error']
    values = [version_id, current_timestamp, nombre_modelo, dataset_name, execution_state, mensaje_error]

    # Agregar json_version_id si se proporciona
    if json_version_id is not None:
        columns.append('json_version_id')
        values.append(json_version_id)

    # Agregar dataset_id si se proporciona
    if dataset_id is not None:
        columns.append('dataset_id')
        values.append(dataset_id)

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



def agregar_datos_model_execution_por_id_validacion_scoring(id_validacion_scoring,  name, nombre_dataset, estado):
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
    columns = ['id_validacion_sc', 'execution_date', 'model_name', 'dataset_name', 'execution_state']
    values = [id_validacion_scoring, current_timestamp, nombre_modelo, dataset_name, execution_state]

    
    add = insert_into_table(table_name, columns, values)
    
    print("REGISTRO INSERT")

    # Retornar el ID del registro insertado
    return add

def agregar_datos_model_execution_scoring(id_score, name, nombre_dataset, estado):
    """
    Actualiza un registro en la tabla 'scoring' basado en el ID de score.

    :param id_score: ID del registro en la tabla 'scoring' que se debe actualizar.
    :param name: Nombre del modelo.
    :param nombre_dataset: Nombre del dataset.
    :param estado: Estado de la ejecución (por ejemplo, 'Éxito', 'Error', etc.).
    :return: Cantidad de registros actualizados.
    """
    # Verificar si el id_score es válido antes de actualizar
    if id_score is None:
        raise ValueError("El ID de score no puede ser None")

    # Conectar a la base de datos dentro de la función
    connection = sqlite3.connect("Modeling_App.db")

    try:
        # Obtener la fecha actual
        current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Llamar a la función genérica update_table()
        registros_actualizados = update_table(
            table_name="scoring",
            update_values={
                "model_name": name,
                "nombre_dataset": nombre_dataset,
                "execution_state": estado,
                "fecha_de_ejecucion": current_timestamp
            },
            where_conditions={"id_score": id_score},
            connection=connection
        )

        print(f"Registro actualizado para id_score {id_score} con fecha {current_timestamp}")
        return registros_actualizados  # Retorna la cantidad de registros actualizados

    except sqlite3.Error as e:
        print(f"Error al actualizar la tabla 'scoring': {e}")
        return 0

    finally:
        connection.close() 

def check_execution_status(db_path, version_id=None, json_id=None, id_validacion_sc=None, score_id=None):
    """
    Verifica el estado de ejecución de un modelo en la base de datos SQLite.

    :param db_path: Ruta al archivo de la base de datos.
    :param version_id: (Opcional) ID de la versión del modelo en 'model_execution'.
    :param json_id: (Opcional) ID del JSON de la versión en 'model_execution' o 'scoring'.
    :param id_validacion_sc: (Opcional) ID del dataset en 'model_execution'.
    :param score_id: (Opcional) ID del score en 'scoring'.
    :return: Estado de ejecución del modelo si existe, None si no se encuentra.
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    try:
        # Si score_id es None, descartamos la consulta a 'scoring'
        if score_id is not None and isinstance(score_id, int):
            query = "SELECT execution_state FROM scoring WHERE id_score = ?"
            cur.execute(query, (score_id,))
            result = cur.fetchone()
            if result:
                return result[0]

        # Si version_id, json_id o id_validacion_sc son None, descartamos la consulta a 'model_execution'
        params = []
        query = "SELECT execution_state FROM model_execution WHERE 1=1"

        if version_id is not None and isinstance(version_id, int):
            query += " AND version_id = ?"
            params.append(version_id)

        if json_id is not None and isinstance(json_id, int):
            query += " AND json_version_id = ?"
            params.append(json_id)

        if id_validacion_sc is not None and isinstance(id_validacion_sc, int):
            query += " AND id_validacion_sc = ?"
            params.append(id_validacion_sc)

        # Solo ejecutamos la consulta si hay condiciones válidas
        if params:
            print(f"🔎 Buscando en 'model_execution' con {params}")
            cur.execute(query, params)
            result = cur.fetchone()
            return result[0] if result else None

        print("⚠️ Ningún parámetro válido fue proporcionado, devolviendo None")
        return None

    except sqlite3.Error as e:
        print(f"❌ Error al consultar la base de datos: {e}")
        return None

    finally:
        conn.close()


def monitorizar_archivo(path, nombre_archivo):
    """
    Lee el último porcentaje de progreso de un archivo y lo retorna.
    Si el archivo existe, lo borra antes de crearlo de nuevo.

    :param path: Ruta del directorio donde se encuentra el archivo.
    :param nombre_archivo: Nombre del archivo a monitorizar.
    :return: Último porcentaje de progreso en formato "X%" o "0%" si no hay progreso registrado.
    """
    archivo_path = os.path.join(path, nombre_archivo)

    # Si el archivo existe, eliminarlo
    if os.path.exists(archivo_path):
        try:
            os.remove(archivo_path)
        except Exception as e:
            print(f"Error al eliminar el archivo '{archivo_path}': {str(e)}")
            return "0%"  # En caso de error al borrar, devolver 0%

    # Crear un archivo vacío para iniciar desde 0 si se necesita
    try:
        with open(archivo_path, "w") as f:
            f.write("")  # Se crea un archivo vacío
        print(f"✅ Archivo '{archivo_path}' creado nuevamente.")
    except Exception as e:
        print(f"❌ Error al crear el archivo '{archivo_path}': {str(e)}")
        return "0%"  # En caso de error, devolver 0%

    return "0%"  # Siempre inicia en 0% al recrear el archivo
