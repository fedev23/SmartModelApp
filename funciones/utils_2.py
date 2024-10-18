import subprocess
import os
import pandas as pd
from clases.loadJson import LoadJson
from shiny import App, ui, reactive
from zipfile import ZipFile, ZIP_DEFLATED
import zipfile
import webbrowser
import os
import shutil
import platform
import asyncio


def errores(mensaje):
    if mensaje.get():
        ui.notification_show(
            ui.p("Error:", style="color: red;"),
            action=ui.p(mensaje.get(), style="font-style: italic;"),
            duration=None,
            close_button=True
            # type='message',
        )


def cambiarAstring(nombre_input):
    # Verificar si el input es un tuple
    input = ', '.join(map(str, nombre_input))
    print( input ,"estoy en la funcion")
    return input



def trans_nulos_adic(input_name):
    # Recorre cada valor de input_name, conviértelo a string y agrega " = 0"
    input_values = ', '.join(f"{str(value)} = 0" for value in input_name)
    print(input_values)
    return input_values

def validar_proyecto(nombre_proyecto):
    if not nombre_proyecto:  # Esto verifica si está vacío o None
        return False
    # Aquí puedes agregar más lógica de validación si es necesario
    return True  # 


def mostrar_error(mensaje_error):
    if mensaje_error:
        ui.notification_show(
            ui.p("Error:", style="color: red;"),
            action=ui.p(mensaje_error, style="font-style: italic;"),
            duration=7,
            close_button=True
        )
        
        
        


# Crear carpetas por ID de usuario
def crear_carpetas_por_id_user(user_id):
    user_id_cleaned = user_id.replace('|', '_')
    base_folder_path = '/path/to/your/base/folder'
    
    entrada_folder = os.path.join(base_folder_path, f"datos_entrada_{user_id_cleaned}")
    salida_folder = os.path.join(base_folder_path, f"datos_salida_{user_id_cleaned}")
    
    if not os.path.exists(entrada_folder):
        os.makedirs(entrada_folder)
        print(f"Carpeta creada {entrada_folder}")
    
    if not os.path.exists(salida_folder):
        os.makedirs(salida_folder)
        print(f"Carpeta creada {salida_folder}")
    
    return user_id_cleaned