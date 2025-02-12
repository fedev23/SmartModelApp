import os
from shiny import App, ui, reactive
import os
import jwt
import pandas as pd
import csv 

from clases.global_reactives import global_estados


def errores(mensaje):
    if mensaje.get():
        ui.notification_show(
            ui.p("Error:", style="color: red;"),
            action=ui.p(mensaje.get(), style="font-style: italic;"),
            duration=None,
            close_button=True
            # type='message',
        )

def to_empty_list(input_value):
    return []
    
 
def cambiarAstring(nombre_input):
    # Verificar si el input es un tuple
    input = ', '.join(map(str, nombre_input))
    return input

def get_equal_from_tuple(value):
    """
    Extrae el símbolo '=' del contenido de una tupla separándolo por una coma.
    
    :param value: Una tupla que contiene un string.
    :return: El valor '=' si existe, de lo contrario un mensaje de error.
    """
    if isinstance(value, tuple):  # Verifica que sea una tupla
        if len(value) > 0:  # Verifica que no esté vacía
            # Toma el primer elemento y lo divide por la coma
            parts = value[0].split(',')
            if len(parts) > 1:  # Verifica que haya al menos dos partes
                return parts[1].strip()  # Devuelve la segunda parte limpia de espacios

def trans_nulos_adic(input_name):
    # Recorre cada valor de input_name, conviértelo a string y agrega " = 0"
    input_values = ', '.join(f"{str(value)} = 0" for value in input_name)
    print(input_values)
    return input_values

def validar_proyecto(id):
    if not id:  # Esto verifica si está vacío o None
        return False
    return True  # 


def mostrar_error(mensaje_error):
    if mensaje_error:
        ui.notification_show(
            ui.p("Error:", style="color: red;"),
            action=ui.p(mensaje_error, style="font-style: italic;"),
            duration=7,
            close_button=True
        )
        
        
        
def detectar_delimitador(file_path):
        """Detecta el delimitador de un archivo de texto o CSV automáticamente."""
        with open(file_path, 'r') as file:
            dialect = csv.Sniffer().sniff(file.readline(), delimiters=";,|\t")
            print(dialect.delimiter)
            return dialect.delimiter
        
# Crear carpetas por ID de usuario
def crear_carpetas_por_id_user(user_id):
    user_id_cleaned = user_id.replace('|', '_')
    base_folder_path = r'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat'
    
    entrada_folder = os.path.join(base_folder_path, f"datos_entrada_{user_id_cleaned}")
    salida_folder = os.path.join(base_folder_path, f"datos_salida_{user_id_cleaned}")
    
    if not os.path.exists(entrada_folder):
        os.makedirs(entrada_folder)
        print(f"Carpeta creada {entrada_folder}")
    
    if not os.path.exists(salida_folder):
        os.makedirs(salida_folder)
        print(f"Carpeta creada {salida_folder}")
    
    return user_id_cleaned

def crear_carpeta_proyecto(user_id, proyecto_id, name_proyect):
    # Limpiar el user_id reemplazando cualquier '|' por '_'
    user_id_cleaned = user_id.replace('|', '_')
    # Definir la ruta base para las carpetas de usuario
    base_folder_path = r'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat'
    
    # Rutas para las carpetas de entrada y salida del usuario
    entrada_folder = os.path.join(base_folder_path, f"datos_entrada_{user_id_cleaned}")
    salida_folder = os.path.join(base_folder_path, f"datos_salida_{user_id_cleaned}")
    
    # Rutas para las subcarpetas del proyecto dentro de cada carpeta del usuario
    entrada_proyecto_folder = os.path.join(entrada_folder, f"proyecto_{proyecto_id}_{name_proyect}")
    salida_proyecto_folder = os.path.join(salida_folder, f"proyecto_{proyecto_id}_{name_proyect}")
    
    # Crear la subcarpeta del proyecto en entrada si no existe
    if not os.path.exists(entrada_proyecto_folder):
        os.makedirs(entrada_proyecto_folder)
        print(f"Carpeta creada {entrada_proyecto_folder}")
    
    # Crear la subcarpeta del proyecto en salida si no existe
    if not os.path.exists(salida_proyecto_folder):
        os.makedirs(salida_proyecto_folder)
        print(f"Carpeta creada {salida_proyecto_folder}")
    
    # Crear la carpeta 'datasets' dentro de la carpeta del proyecto en entrada
    datasets_folder = os.path.join(entrada_proyecto_folder, "datasets")
    if not os.path.exists(datasets_folder):
        os.makedirs(datasets_folder)
        print(f"Carpeta creada {datasets_folder}")
    
    # Retornar la ruta de las carpetas de proyecto y datasets
    return  datasets_folder



def crear_carpeta_version_por_proyecto(user_id, proyecto_id, version_id, name_id, name_proyect):
    # Limpiar el user_id reemplazando cualquier '|' por '_'
    user_id_cleaned = user_id.replace('|', '_')

    # Definir la ruta base para las carpetas de usuario
    base_folder_path = r'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat'

    # Rutas para las carpetas de entrada y salida del usuario
    entrada_folder = os.path.join(base_folder_path, f"datos_entrada_{user_id_cleaned}")
    salida_folder = os.path.join(base_folder_path, f"datos_salida_{user_id_cleaned}")

    # Rutas para las subcarpetas del proyecto dentro de cada carpeta del usuario
    entrada_proyecto_folder = os.path.join(entrada_folder, f"proyecto_{proyecto_id}_{name_proyect}")
    salida_proyecto_folder = os.path.join(salida_folder, f"proyecto_{proyecto_id}_{name_proyect}")

    # Rutas para las subcarpetas de la versión dentro del proyecto
    entrada_version_folder = os.path.join(entrada_proyecto_folder, f"version_{version_id}_{name_id}")
    salida_version_folder = os.path.join(salida_proyecto_folder, f"version_{version_id}_{name_id}")

    # Crear las subcarpetas del proyecto en entrada si no existen
    if not os.path.exists(entrada_version_folder):
        os.makedirs(entrada_version_folder)
        print(f"Carpeta creada {entrada_version_folder}")

    # Crear las subcarpetas del proyecto en salida si no existen
    if not os.path.exists(salida_version_folder):
        os.makedirs(salida_version_folder)
        print(f"Carpeta creada {salida_version_folder}")

    # Retornar la ruta de las carpetas de la versión
    return entrada_version_folder, salida_version_folder


def crear_carpeta_version_parametros(user_id, proyecto_id, version_id, id_param, name_param, name_proyect, name_version):
    # Limpiar el user_id reemplazando cualquier '|' por '_'
    user_id_cleaned = user_id.replace('|', '_')

    # Definir la ruta base para las carpetas de usuario
    base_folder_path = r'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat'

    # Rutas para las carpetas de entrada y salida del usuario
    entrada_folder = os.path.join(base_folder_path, f"datos_entrada_{user_id_cleaned}")
    salida_folder = os.path.join(base_folder_path, f"datos_salida_{user_id_cleaned}")

    # Rutas para las subcarpetas del proyecto dentro de cada carpeta del usuario
    entrada_proyecto_folder = os.path.join(entrada_folder, f"proyecto_{proyecto_id}_{name_proyect}")
    salida_proyecto_folder = os.path.join(salida_folder, f"proyecto_{proyecto_id}_{name_proyect}")

    # Rutas para las subcarpetas de la versión dentro del proyecto
    entrada_version_folder = os.path.join(entrada_proyecto_folder, f"version_{version_id}_{name_version}")
    salida_version_folder = os.path.join(salida_proyecto_folder, f"version_{version_id}_{name_version}")

    # Ruta para la nueva carpeta de versión de parámetros
    version_param_folder_name = f"version_parametros_{id_param}_{name_param}"
    entrada_version_param_folder = os.path.join(entrada_version_folder, version_param_folder_name)
    salida_version_param_folder = os.path.join(salida_version_folder, version_param_folder_name)

    # Crear la carpeta de versión de parámetros en entrada si no existe
    if not os.path.exists(entrada_version_param_folder):
        os.makedirs(entrada_version_param_folder)
        print(f"Carpeta creada {entrada_version_param_folder}")

    # Crear la carpeta de versión de parámetros en salida si no existe
    if not os.path.exists(salida_version_param_folder):
        os.makedirs(salida_version_param_folder)
        print(f"Carpeta creada {salida_version_param_folder}")

    # Retornar la ruta de las carpetas de la versión de parámetros
    return entrada_version_param_folder, salida_version_param_folder


def crear_carpeta_validacion_scoring(user_id, proyecto_id, version_id, id_param, name_param, name_proyect, name_version, name_dataset):
    # Limpiar el user_id reemplazando cualquier '|' por '_'
    user_id_cleaned = user_id.replace('|', '_')

    # Definir la ruta base para las carpetas de usuario
    base_folder_path = r'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat'

    # Rutas para las carpetas de entrada y salida del usuario
    entrada_folder = os.path.join(base_folder_path, f"datos_entrada_{user_id_cleaned}")
    salida_folder = os.path.join(base_folder_path, f"datos_salida_{user_id_cleaned}")

    # Rutas para las subcarpetas del proyecto dentro de cada carpeta del usuario
    entrada_proyecto_folder = os.path.join(entrada_folder, f"proyecto_{proyecto_id}_{name_proyect}")
    salida_proyecto_folder = os.path.join(salida_folder, f"proyecto_{proyecto_id}_{name_proyect}")

    # Rutas para las subcarpetas de la versión dentro del proyecto
    entrada_version_folder = os.path.join(entrada_proyecto_folder, f"version_{version_id}_{name_version}")
    salida_version_folder = os.path.join(salida_proyecto_folder, f"version_{version_id}_{name_version}")

    # Ruta para la nueva carpeta de versión de parámetros
    version_param_folder_name = f"version_parametros_{id_param}_{name_param}"
    entrada_version_param_folder = os.path.join(entrada_version_folder, version_param_folder_name)
    salida_version_param_folder = os.path.join(salida_version_folder, version_param_folder_name)
    
    
    entrada_data_set_name_path = os.path.join(entrada_version_param_folder, name_dataset)
    salida_data_set_name_path = os.path.join(salida_version_param_folder, name_dataset)


    # Crear la carpeta de versión de parámetros en entrada si no existe
    if not os.path.exists(entrada_data_set_name_path):
        os.makedirs(entrada_data_set_name_path)
        print(f"Carpeta creada {entrada_data_set_name_path}")

    # Crear la carpeta de versión de parámetros en salida si no existe
    if not os.path.exists(salida_data_set_name_path):
        os.makedirs(salida_data_set_name_path)
        print(f"Carpeta creada {salida_data_set_name_path}")

    # Retornar la ruta de las carpetas de la versión de parámetros
    return entrada_data_set_name_path, salida_data_set_name_path



def get_user_directory(user_id):
    user_id_cleaned = user_id.replace('|', '_')
    base_directory = r'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat'
    user_directory = os.path.join(base_directory, f'datos_entrada_{user_id_cleaned}')
    
    # Verificar si el directorio existe antes de devolverlo
    if os.path.exists(user_directory):
        return user_directory
    else:
        print(f"El directorio {user_directory} no existe.")
        return None
    
    
def get_datasets_directory(user_id, proyecto_id, name_proyect):
    # Limpiar el user_id reemplazando cualquier '|' por '_'
    user_id_cleaned = user_id
    base_directory = r'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat'
    
    # Construir la ruta de la carpeta de entrada del usuario
    entrada_folder = os.path.join(base_directory, f'datos_entrada_{user_id_cleaned}')
    
    # Construir la ruta de la carpeta del proyecto dentro de la carpeta de entrada
    proyecto_folder = os.path.join(entrada_folder, f"proyecto_{proyecto_id}_{name_proyect}")
    
    
    # Construir la ruta de la carpeta 'datasets' dentro del proyecto
    datasets_folder = os.path.join(proyecto_folder, 'datasets')
    
    
    print(f'dataser: {datasets_folder}')
    
    # Verificar si la carpeta 'datasets' existe antes de devolverla
    if os.path.exists(datasets_folder):
        return datasets_folder
    else:
        print(f"La carpeta {datasets_folder} no existe.")
        return None
    
def leer_dataset(user_id, proyecto_id, name_proyect, dataset_name, nombre_version, version_Id):
    """

    Lee un dataset basado en el usuario, proyecto y nombre del dataset.

    Args:
        user_id (str): ID del usuario.
        proyecto_id (str): ID del proyecto.
        name_proyect (str): Nombre del proyecto.
        dataset_name (str): Nombre del archivo del dataset.

    Returns:
        pd.DataFrame: Las primeras 10 filas del dataset si se encuentra, o un DataFrame vacío.
    """
    try:
        # Obtener la ruta de la carpeta de datasets
        print(user_id, proyecto_id, name_proyect, nombre_version, version_Id)
        print(dataset_name)
        datasets_directory = get_datasets_directory(user_id, proyecto_id, name_proyect)
        
        # Verificar que la carpeta de datasets no sea None
        if datasets_directory is None:
            print(f"No se encontró la carpeta de datasets. {datasets_directory}")
            return pd.DataFrame()  # Retornar un DataFrame vacío
        
        # Construir la ruta completa del archivo del dataset
        dataset_path = os.path.join(datasets_directory, dataset_name)
        
        # Verificar que el archivo existe
        if not os.path.exists(dataset_path):
            print(f"El archivo {dataset_path} no existe.")
            return pd.DataFrame()  # Retornar un DataFrame vacío
            
        # Leer el archivo de datos usando pandas
        try:
            # Detectar el delimitador del archivo
            delimitador = detectar_delimitador(dataset_path)
            global_estados.set_delimitador(delimitador)
            
            # Leer el archivo con el delimitador detectado
            dataset = pd.read_csv(dataset_path, delimiter=delimitador)
            print(f"Dataset {dataset_name} leído correctamente.")
            
            # Retornar las primeras 10 filas del dataset
            return dataset

        except Exception as e:
            print(f"Error al leer el dataset: {e}")
            return pd.DataFrame()

    except Exception as e:
        # Manejo global de errores
        print(f"Error inesperado en leer_dataset: {e}")
        return pd.DataFrame()


def render_data_summary(data):
    if data is None or data.empty:
        # Retornar un DataFrame vacío para evitar errores en Shiny
        print("Advertencia: 'data' es None o un DataFrame vacío.")
        return pd.DataFrame()  # Retorna un DataFrame vacío

    valor_Defult = 5
    select_number_data_set = int(global_estados.get_numero_dataset())
    return pd.DataFrame(data.head(select_number_data_set))        
        
def aplicar_transformaciones(input, transformaciones):
    inputs_procesados = {}
    for key, transformacion in transformaciones.items():
        # Aplica la transformación a cada input
        inputs_procesados[key] = transformacion(input[key]())
    return inputs_procesados


def crear_carpeta_dataset(path):
    """
    Crea un folder llamado 'datasets' dentro del path especificado.

    Args:
        path (str): Ruta del folder donde se creará el subfolder 'datasets'.

    Returns:
        str: Ruta completa del folder 'datasets' creado.

    Raises:
        FileNotFoundError: Si el folder especificado en 'path' no existe.
        Exception: Si ocurre un error al crear el folder 'datasets'.
    """
    try:
        # Verificar si el path existe
        if not os.path.exists(path):
            raise FileNotFoundError(f"El folder especificado no existe: {path}")

        # Crear el folder 'datasets'
        dataset_folder = os.path.join(path, "datasets")
        os.makedirs(dataset_folder, exist_ok=True)

        print(f"Folder 'datasets' creado en: {dataset_folder}")
        return dataset_folder

    except Exception as e:
        print(f"Error al crear el folder 'datasets': {e}")
        raise


    
def get_folder_directory_data_validacion_scoring(user_id, proyecto_id, name_proyect, version_name, version_id, id_niveles_y_scord, nombre_niveles_scord, nombre_data):
    # Limpiar el user_id reemplazando cualquier '|' por '_'
    user_id_cleaned = user_id
    base_directory = r'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat'
    
    # Construir la ruta de la carpeta de entrada del usuario
    entrada_folder = os.path.join(base_directory, f'datos_entrada_{user_id_cleaned}')
    
    # Construir la ruta de la carpeta del proyecto dentro de la carpeta de entrada
    proyecto_folder = os.path.join(entrada_folder, f"proyecto_{proyecto_id}_{name_proyect}")
    
    version_folder = os.path.join(proyecto_folder, f"version_{version_id}_{version_name}")
    
    version_niveles_y_scord = os.path.join(version_folder, f"version_parametros_{id_niveles_y_scord}_{nombre_niveles_scord}")
    # Construir la ruta de la carpeta 'datasets' dentro del proyecto
    datasets_folder = os.path.join(version_niveles_y_scord, nombre_data)
        
    
    
    # Verificar si la carpeta 'datasets' existe antes de devolverla
    if os.path.exists(datasets_folder):
        return datasets_folder
    else:
        print(f"La carpeta {datasets_folder} no existe.")
        return None



def get_folder_directory_data_validacion_scoring_SALIDA(user_id, proyecto_id, name_proyect, version_name, version_id, id_niveles_y_scord, nombre_niveles_scord, nombre_data):
    """
    Genera los paths de entrada y salida basados en los valores proporcionados.

    :param user_id: ID del usuario.
    :param proyecto_id: ID del proyecto.
    :param name_proyect: Nombre del proyecto.
    :param version_name: Nombre de la versión.
    :param version_id: ID de la versión.
    :param id_niveles_y_scord: ID de niveles y scoring.
    :param nombre_niveles_scord: Nombre de niveles y scoring.
    :param nombre_data: Nombre del archivo de datos.
    :return: Tupla con (path_datos_entrada, path_datos_salida)
    """
    # Base del directorio
    base_directory = r'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat'

    # Normalizar `user_id` si contiene caracteres especiales
    user_id_cleaned = user_id.replace("|", "_")

    # 📌 **Path de Entrada**
    entrada_folder = os.path.join(base_directory, f'datos_entrada_{user_id_cleaned}')
    proyecto_folder = os.path.join(entrada_folder, f"proyecto_{proyecto_id}_{name_proyect}")
    version_folder = os.path.join(proyecto_folder, f"version_{version_id}_{version_name}")
    version_niveles_y_scord = os.path.join(version_folder, f"version_parametros_{id_niveles_y_scord}_{nombre_niveles_scord}")
    path_datos_entrada = os.path.join(version_niveles_y_scord, nombre_data)

    # 📌 **Path de Salida**
    salida_folder = os.path.join(base_directory, f'datos_salida_{user_id_cleaned}')
    proyecto_folder_salida = os.path.join(salida_folder, f"proyecto_{proyecto_id}_{name_proyect}")
    version_folder_salida = os.path.join(proyecto_folder_salida, f"version_{version_id}_{version_name}")
    version_niveles_y_scord_salida = os.path.join(version_folder_salida, f"version_parametros_{id_niveles_y_scord}_{nombre_niveles_scord}")
    path_datos_salida = os.path.join(version_niveles_y_scord_salida, nombre_data)

    return path_datos_entrada, path_datos_salida
    
    
    # Verificar si la carpeta 'datasets' existe antes de devolverla
    if os.path.exists(datasets_folder):
        return datasets_folder
    else:
        print(f"La carpeta {datasets_folder} no existe.")
        return None



def eliminar_archivo(nombre_archivo):
    """
    Elimina un archivo dado su nombre.
    
    Args:
        nombre_archivo (str): Ruta completa o nombre del archivo a eliminar.
        
    Returns:
        str: Mensaje indicando si el archivo fue eliminado o no.
    """
    try:
        if os.path.exists(nombre_archivo):
            os.remove(nombre_archivo)
            return f"El archivo '{nombre_archivo}' ha sido eliminado con éxito."
        else:
            return f"El archivo '{nombre_archivo}' no existe."
    except Exception as e:
        return f"Error al intentar eliminar el archivo '{nombre_archivo}': {e}"