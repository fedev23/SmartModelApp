
from clases.global_session import global_session
from funciones.utils_2 import get_datasets_directory
import asyncio
from clases.class_cargar_datos import CargarDatos
from clases.data_loader import DataLoader

async def guardar_archivo(file_func, name):
    # Obtén el directorio en el que se debe guardar el archivo
    datos = global_session.get_path_guardar_dataSet_en_proyectos()
    print(datos, "datos en get")
    file_info = file_func()
    
    # Construye el path del dataset donde se guardará el archivo
    data_Set = get_datasets_directory(
        global_session.get_id_user(), 
        global_session.get_id_proyecto(), 
        global_session.get_name_proyecto()
    )
    
    # Instancia el DataLoader con el nombre del archivo
    data_loader = DataLoader(name)
    
    try:
        # Llamamos al método asincrónico cargar_archivos de DataLoader
        df, cargado = await data_loader.cargar_archivos(file_info, datos)
        
        if cargado:
            # Aquí ya tenemos los datos cargados, y ahora los guardamos
            # Nota: `df` es el DataFrame cargado, puedes usarlo si es necesario
            print(f"Archivo cargado y procesado correctamente")
            
            # Retorna el path donde se guardó el archivo
            return datos
        else:
            print("No se pudo cargar el archivo correctamente.")
            raise ValueError("Error al cargar los datos.")
    
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")
        raise