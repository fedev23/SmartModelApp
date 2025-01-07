from clases.class_cargar_datos import CargarDatos
import os
from shiny import ui
from clases.global_session import *
from clases.global_name import global_name_manager
from api.db import *
from clases.reactives_name import *
from datetime import datetime
#from funciones.cargar_archivosNEW import cargar_archivos
import shutil


def cargar_archivos(file_info, directorio):
    print("Cargando datos...")

    if not file_info:
        print("No se seleccionó ningún archivo.")
        raise ValueError("No se seleccionó ningún archivo")

    # Instanciar la clase CargarDatos
    cargador = CargarDatos(file_info, directorio)

    try:
        # Usar el método cargar_datos de la instancia CargarDatos
        file_name, archivo_guardado = cargador.cargar_datos()
        print(f'Se ha guardado el archivo {archivo_guardado}.')
        
        # Devuelve el DataFrame cargado y otros datos necesarios
        return file_name, archivo_guardado
    except Exception as e:
        print(f"Error al cargar datos: {e}")
        raise


def mover_y_renombrar_archivo(nombre_archivo, directorio_base, name_suffix, destino_base):
    """
    Busca un archivo, lo copia al destino con un nuevo nombre y mantiene el original en el lugar.

    :param nombre_archivo: Nombre del archivo (incluyendo la extensión).
    :param directorio_base: Directorio donde se buscará el archivo.
    :param name_suffix: Sufijo que define el nuevo nombre del archivo.
    :param destino_base: Directorio base donde se copiará el archivo.
    :return: Ruta completa del archivo en el destino.
    """
    try:
        # Verificar que el directorio base exista
        if not os.path.isdir(directorio_base):
            raise FileNotFoundError(f"El directorio base no existe: {directorio_base}")
        
        # Ruta completa del archivo de origen
        file_path = os.path.join(directorio_base, nombre_archivo)

        # Verificar si el archivo existe
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"No se encontró el archivo '{nombre_archivo}' en: {directorio_base}")

        # Asegurarse de que el directorio de destino exista
        os.makedirs(destino_base, exist_ok=True)

        # Determinar el nuevo nombre del archivo según el sufijo
        if name_suffix == 'validacion':
            nuevo_nombre = "Muestra_Validación.txt"
        elif name_suffix == 'produccion':
            nuevo_nombre = "Muestra_Scoring.txt"
        elif name_suffix == 'desarrollo':
            nuevo_nombre = "Muestra_Desarrollo.txt"
        elif name_suffix == 'in_sample':
            nuevo_nombre = "Muestra_Desarrollo.txt"
        else:
            raise ValueError(f"Sufijo desconocido: {name_suffix}")

        # Ruta completa del archivo destino
        ruta_destino = os.path.join(destino_base, nuevo_nombre)

        # Copiar el archivo al destino con el nuevo nombre
        shutil.copy2(file_path, ruta_destino)

        print(f"Archivo copiado y renombrado: {ruta_destino}")
        return ruta_destino

    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except ValueError as e:
        print(f"Error de valor: {e}")
        raise
    except Exception as e:
        print(f"Error inesperado en mover files: {e}")
        raise
    
    

def create_modal_warning_exist_file(file_name, name, nombre_version):
        return ui.modal(
            ui.tags.div(
            ui.row(
                ui.column(
                    12,
                    ui.tags.p(
                        f"El archivo '{file_name}' ya existe en la version {nombre_version}.",
                        style="color: #d9534f; font-size: 16px; font-weight: bold; text-align: center; margin-bottom: 20px;"
                    ),
                     style="padding: 10px; border: 1px solid #d9534f; border-radius: 5px; background-color: #f2dede;"
                    
                ),
            )
        ),
            title=ui.tags.div(
            "⚠️ Advertencia",
            style="color: #f0ad4e; font-size: 20px; font-weight: bold; text-align: center;"
        ),
            easy_close=True,
            size='xs',
            footer=ui.input_action_button(f"cancel_overwrite_{name}", "Cancelar", style="margin-left: 10px;")
        )
        


def create_modal_warning_exist_file_for_full_or_sc(file_name, name):
        return ui.modal(
            ui.tags.div(
            ui.row(
                ui.column(
                    12,
                    ui.tags.p(
                        f"El archivo '{file_name}' ya existe en la version en el sistema de archivos."
                    )
                ),
            )
        ),
            title="Advertencia",
            easy_close=True,
            size='xs',
            footer=ui.input_action_button(f"cancel_overwrite_{name}", "Cancelar", style="margin-left: 10px;")
        )