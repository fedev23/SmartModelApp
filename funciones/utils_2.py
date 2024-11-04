import os
from shiny import App, ui, reactive
import os
import jwt


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
    return input



def trans_nulos_adic(input_name):
    # Recorre cada valor de input_name, conviértelo a string y agrega " = 0"
    input_values = ', '.join(f"{str(value)} = 0" for value in input_name)
    print(input_values)
    return input_values

def validar_proyecto(nombre_proyecto):
    if not nombre_proyecto:  # Esto verifica si está vacío o None
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
    




