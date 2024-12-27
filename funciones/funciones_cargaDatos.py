
from clases.global_session import global_session
from funciones.utils_2 import get_datasets_directory_data_set_versiones
import os
from clases.class_cargar_datos import CargarDatos
from clases.data_loader import DataLoader
from clases.class_screens import ScreenClass

async def guardar_archivo(file_func, name):
    # Obtén el directorio en el que se debe guardar el archivo
    directorio = global_session.get_path_guardar_dataSet_en_proyectos()
    print(directorio)
    file_info = file_func()
    
    # Construye el path del dataset donde se guardará el archivo
    directorio_version = get_datasets_directory_data_set_versiones(
        global_session.get_id_user(), 
        global_session.get_id_proyecto(), 
        global_session.get_name_proyecto(),
        global_session.get_versiones_name(),
        global_session.get_id_version()
    )
    
    # Instancia el DataLoader con el nombre del archivo
    path_datos_entrada = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_entrada_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}'
    screen = ScreenClass(path_datos_entrada, name)
    data_loader = DataLoader(name)
    #screen.cambiar_name(nuevo_nombre_archivo, file_info)
    
    try:
        # Llamamos al método asincrónico cargar_archivos de DataLoader
        cargado = await data_loader.cargar_archivos(file_info, directorio_version)
        
        # Intentamos cargar el nombre del archivo con el método de ScreenClass
        nombre_archivo = await screen.load_data(file_func, name)
        
        if not nombre_archivo:
            raise ValueError("El nombre del archivo cargado es inválido o está vacío.")
        
        if cargado:
            # Aquí ya tenemos los datos cargados, y ahora los guardamos
            print(f"Archivo '{nombre_archivo}' cargado y procesado correctamente")
            
            # Retorna el path donde se guardó el archivo
            return directorio, nombre_archivo
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





def verificar_archivo():
    """
    Verifica si hay al menos un archivo en el directorio especificado.

    Args:
        folder_path (str): Ruta del directorio a verificar.

    Returns:
        bool: True si hay al menos un archivo en el directorio, False en caso contrario.
    """
    folder_path = get_datasets_directory_data_set_versiones(
        global_session.get_id_user(), 
        global_session.get_id_proyecto(), 
        global_session.get_name_proyecto(),
        global_session.get_versiones_name(),
        global_session.get_id_version()
    )
    
    
    if not os.path.isdir(folder_path):
        raise ValueError(f"La ruta proporcionada '{folder_path}' no es un directorio válido.")
    
    # Lista de archivos en el directorio
    archivos = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    return len(archivos) > 0    



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