
from clases.global_session import global_session
from funciones.utils_2 import get_datasets_directory
import asyncio
from clases.class_cargar_datos import CargarDatos
from clases.data_loader import DataLoader
from clases.class_screens import ScreenClass

async def guardar_archivo(file_func, name):
    # Obtén el directorio en el que se debe guardar el archivo
    directorio = global_session.get_path_guardar_dataSet_en_proyectos()
    print(directorio, "direcotrio")
    file_info = file_func()
    
    # Construye el path del dataset donde se guardará el archivo
    data_Set = get_datasets_directory(
        global_session.get_id_user(), 
        global_session.get_id_proyecto(), 
        global_session.get_name_proyecto()
    )
    
    # Instancia el DataLoader con el nombre del archivo
    path_datos_entrada = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_entrada_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}'
    screen = ScreenClass(path_datos_entrada, name)
    data_loader = DataLoader(name)
    #screen.cambiar_name(nuevo_nombre_archivo, file_info)
    
    try:
        # Llamamos al método asincrónico cargar_archivos de DataLoader
        cargado = await data_loader.cargar_archivos(file_info, directorio)
        
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



