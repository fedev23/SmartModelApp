
from clases.global_session import global_session
from funciones.utils_2 import get_datasets_directory
import os
from clases.class_cargar_datos import CargarDatos
from clases.data_loader import DataLoader

async def guardar_archivo(file_func, name):
    # Obtén el directorio en el que se debe guardar el archivo
    file_info = file_func()
    
    # Construye el path del dataset donde se guardará el archivo
    directorio = get_datasets_directory(
        global_session.get_id_user(), 
        global_session.get_id_proyecto(), 
        global_session.get_name_proyecto()
    )
    
    # Instancia el DataLoader con el nombre del archivo
    path_datos_entrada = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_entrada_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}'
    #screen = ScreenClass(path_datos_entrada, name)
    data_loader = DataLoader(name)
    #screen.cambiar_name(nuevo_nombre_archivo, file_info)
    
    try:
        # Llamamos al método asincrónico cargar_archivos de DataLoader
        cargado = await data_loader.cargar_archivos(file_info, directorio)
        
        # Intentamos cargar el nombre del archivo con el método de ScreenClass
        #nombre_archivo = await screen.load_data(file_func, name)
        

        
        if cargado:
            return directorio
        else:
            print("No se pudo cargar el archivo correctamente.")
            raise ValueError("Error al cargar los datos.")
        
    except ValueError as ve:
        # Manejo específico de errores de valor (por ejemplo, nombre de archivo inválido)
        print(f"Error en el procesamiento de datos: {ve}")
        raise
    except Exception as e:
        # Manejo genérico de errores inesperados
        print(f"Error al guardar el archivo: {e}")
    raise


async def guardar_archivo_sc(file_func, name):
    # Obtén el directorio en el que se debe guardar el archivo
    data = global_session.get_path_guardar_dataSet_en_proyectos()
    #print(directorio, "direcotrio")
    file_info = file_func()
    
    # Construye el path del dataset donde se guardará el archivo
    directorio = get_datasets_directory(
        global_session.get_id_user(), 
        global_session.get_id_proyecto(), 
        global_session.get_name_proyecto()
    )
    
    # Instancia el DataLoader con el nombre del archivo
    path_datos_entrada = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_entrada_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}'
    #screen = ScreenClass(path_datos_entrada, name)
    data_loader = DataLoader(name)
    #screen.cambiar_name(nuevo_nombre_archivo, file_info)
    
    try:
        # Llamamos al método asincrónico cargar_archivos de DataLoader
        cargado = await data_loader.cargar_archivos(file_info, directorio)
        
        # Intentamos cargar el nombre del archivo con el método de ScreenClass
        #nombre_archivo = await screen.load_data(file_func, name)
        
        
        
        if cargado:
            return directorio
        else:
            print("No se pudo cargar el archivo correctamente.")
            raise ValueError("Error al cargar los datos.")
        
    except ValueError as ve:
        # Manejo específico de errores de valor (por ejemplo, nombre de archivo inválido)
        print(f"Error en el procesamiento de datos: {ve}")
        raise
    except Exception as e:
        # Manejo genérico de errores inesperados
        print(f"Error al guardar el archivo: {e}")
    raise



def verificar_archivo(nombre_archivo):
    """
    Verifica si hay al menos un archivo en el directorio especificado.

    Args:
        folder_path (str): Ruta del directorio a verificar.

    Returns:
        bool: True si hay al menos un archivo en el directorio, False en caso contrario.
    """
    folder_path = get_datasets_directory(
        global_session.get_id_user(), 
        global_session.get_id_proyecto(), 
        global_session.get_name_proyecto(),
    )
    
    
    ruta_completa = os.path.join(folder_path, nombre_archivo)
    
    # Verificar si el archivo existe
    if os.path.isfile(ruta_completa):
        return True
    else:
        return False


def verificar_archivo_sc(path, nombre_archivo):
    """
    Verifica si un archivo existe en un directorio específico.
    
    Args:
        path (str): El directorio donde buscar.
        nombre_archivo (str): El nombre del archivo a buscar.
    
    Returns:
        dict: Un mensaje de error si el archivo existe, de lo contrario, un mensaje de éxito.
    """
    # Construir el path completo del archivo
    ruta_completa = os.path.join(path, nombre_archivo)
    
    # Verificar si el archivo existe
    if os.path.isfile(ruta_completa):
        return True
    else:
        return False