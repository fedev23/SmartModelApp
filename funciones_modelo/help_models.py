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
    ult_model = obtener_ultimo_modelo_por_version(base_datos, id_version)
    print(ult_model, f"ult_model para etapa '{etapa_nombre}'")

    # Obtener el estado del modelo para la etapa
    estado_model = obtener_estado_por_modelo(ult_model, etapa_nombre)
    print(estado_model, f"estado_model para etapa '{etapa_nombre}'")

    # Obtener la fecha del modelo para la etapa
    fecha_model = obtener_fecha_por_modelo(ult_model, etapa_nombre)
    print(fecha_model, f"fecha_model para etapa '{etapa_nombre}'")

    # Retornar el estado y la fecha como una tupla
    return estado_model, fecha_model



from datetime import datetime

def agregar_datos_model_execution(version_id, name, nombre_dataset, estado):
    """
    Inserta un registro en la tabla model_execution con los datos proporcionados.

    :param version_id: ID de la versión actual.
    :param name: Nombre del modelo.
    :param nombre_dataset: Nombre del dataset.
    :param estado: Estado de la ejecución (por ejemplo, 'Exito', 'Error', etc.).
    :return: ID del último registro insertado (add).
    """
    # Valores requeridos para la inserción
    version_id = version_id
    nombre_modelo = name
    dataset_name = nombre_dataset
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    execution_state =  estado # Puedes cambiarlo según corresponda

    # Definir la tabla y las columnas
    table_name = "model_execution"
    columns = ['version_id', 'execution_date', 'model_name', 'dataset_name', 'execution_state']

    # Valores para insertar
    values = [version_id, current_timestamp, nombre_modelo, dataset_name, execution_state]

    # Llamar a la función de inserción
    add = insert_into_table(table_name, columns, values)

    # Retornar el ID del registro insertado
    return add