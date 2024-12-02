import os
import json
from funciones.utils import crear_card_con_input_seleccionador, crear_card_con_input_numeric_2, crear_card_con_input_seleccionador_V2, crear_card_con_input_seleccionador_V3
from shiny import ui
from clases.global_sessionV2 import  *


def get_datasets_directory_json(user_id, proyecto_id, name_proyect, id_version, nombre_version):
    # Limpiar el user_id reemplazando cualquier '|' por '_'
    user_id_cleaned = user_id.replace('|', '_')
    
    # Ruta base
    base_directory = r'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat'
    
    # Construir la ruta de la carpeta de entrada del usuario
    entrada_folder = os.path.join(base_directory, f'datos_entrada_{user_id_cleaned}')
    
    # Construir la ruta de la carpeta del proyecto dentro de la carpeta de entrada
    proyecto_folder = os.path.join(entrada_folder, f"proyecto_{proyecto_id}_{name_proyect}")
    
    # Corregir el error de os.path.joi -> os.path.join
    version_folder = os.path.join(proyecto_folder, f'version_{id_version}_{nombre_version}')
    
    # Construir la ruta de la carpeta 'datasets' dentro del proyecto
    datasets_folder = os.path.join(version_folder)
    
    print(datasets_folder , "viendo datos en ger_directory")
    # Verificar si la carpeta 'datasets' existe antes de devolverla
    if os.path.exists(datasets_folder):
        return datasets_folder
    else:
        print(f"La carpeta {datasets_folder} no existe.")
        return None



def leer_control_json(user_id, proyecto_id, name_proyect, id_version, nombre_version):
    # Obtener la ruta de la carpeta de datasets (o de la versión y proyecto)
    version_folder = get_datasets_directory_json(user_id, proyecto_id, name_proyect, id_version, nombre_version)
    
    # Verificar que la carpeta de la versión no sea None
    if version_folder is None:
        print(f"No se encontró la carpeta de la versión del proyectooo. {version_folder}")
        return None  # Retornar None si no se encontró la carpeta
    
    # Construir la ruta completa del archivo JSON
    control_json_path = os.path.join(version_folder, 'Control de SmartModelStudio.json')
    
    #print(control_json_path, "viendo el path de json!!")
    # Verificar que el archivo JSON exista
    if not os.path.exists(control_json_path):
        print(f"El archivo {control_json_path} no existe.")
        return None  # Retornar None si el archivo no existe
    
    # Leer el archivo JSON
    try:
        with open(control_json_path, 'r', encoding='utf-8') as file:
            control_data = json.load(file)
        print(f"Archivo JSON {control_json_path} leído con éxito.")
        return control_data  # Retornar el contenido del archivo JSON
    
    except Exception as e:
        print(f"Error al leer el archivo JSON: {e}")
        return None
    

def get_parameter_value(parameter_name, lista):
    # Buscar el diccionario que tiene el nombre del parámetro
    param = next((item for item in lista if item['parameter'] == parameter_name), None)
    if param:
        return param['value']
    return None


def update_selectize_from_columns_and_json(column_names, selectize_params, json_params=None):
    """
    Actualiza los selectores con las columnas disponibles y valores seleccionados del JSON.

    Args:
        column_names (list): Lista de nombres de columnas disponibles.
        selectize_params (dict): Diccionario con los IDs de selectores y los nombres de parámetros en el JSON.
        json_params (dict, optional): Parámetros cargados desde el JSON. Default es None.
    """
    # Actualiza siempre las opciones disponibles en los selectores
    for selectize_id in selectize_params.keys():
        ui.update_selectize(selectize_id, choices=column_names, selected=[])

    # Si hay parámetros en el JSON, actualiza los valores seleccionados
    if json_params:
        for selectize_id, param_name in selectize_params.items():
            # Obtén el valor del parámetro
            value = get_parameter_value(param_name, json_params)

            # Procesa el valor si es una cadena con elementos separados por comas
            if isinstance(value, str):
                value = [v.strip() for v in value.split(",")]

            # Actualiza el selectize con los valores seleccionados
            ui.update_selectize(selectize_id, choices=column_names, selected=value)
            

def parametros_sin_version(name_suffix):
    return ui.div(
        ui.output_ui(f"acordeon_columnas_{name_suffix}"),
        ui.card(
            ui.row(
                # Fila 1
                crear_card_con_input_seleccionador("par_ids", "Columnas identificadora:", "help_columnas_id", 
                                                   ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px")),
                crear_card_con_input_numeric_2(f"par_split", "Training and Testing", "help_training_testing", 
                                               ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"), 
                                               [], default_value=0, min_value=0, max_value=2, step=0.01),
                crear_card_con_input_seleccionador("par_target", "Columna Target", "help_target_col", 
                                                   ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px")),
                
                # Fila 2
                crear_card_con_input_seleccionador(f"cols_forzadas_a_predictoras", "Variables forzadas a variables candidatas", 
                                                   "help_vars_forzadas", ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px")),
                crear_card_con_input_seleccionador(f"cols_forzadas_a_cat", "Columnas forzadas a categorías", 
                                                   "help_cols_forzadas_a_cat", ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px")),
                crear_card_con_input_seleccionador(f"par_var_grupo", "Define grupos para evaluar las candidatas", 
                                                   "help_par_var_grupo", ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px")),
                
                # Fila 3
                crear_card_con_input_seleccionador("cols_nulos_adic", "Lista de variables y códigos de nulos", 
                                                      "help_nulos_adic", ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px")),
                crear_card_con_input_numeric_2(f"par_cor_show", "Mostrar variables por alta correlación:", "help_par_cor_show", 
                                               ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"), 
                                               [], default_value=0, min_value=0, max_value=1, step=0.01),
                crear_card_con_input_numeric_2(f"par_iv", "Límite para descartar variables por bajo IV", "help_iv", 
                                               ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"), 
                                               [], default_value=3, min_value=0.5, max_value=10, step=0.1),
                
                # Fila 4
                crear_card_con_input_seleccionador_V2(f"cols_no_predictoras", "Columnas excluidas del modelo", 
                                                      "help_cols_no_predictoras", ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px")),
                crear_card_con_input_numeric_2(f"par_cor", "Descartar variables por alta correlación", "help_par_cor", 
                                               ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"), 
                                               [], default_value=3, min_value=0.5, max_value=10, step=0.1),
                crear_card_con_input_numeric_2(f"par_minpts1", "Casos mínimos de bin de primera etapa", "help_minpts", 
                                               ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"), 
                                               [], default_value=3, min_value=0.5, max_value=10, step=0.1)
            ),
            ui.output_ui(f"error_{name_suffix}"),
        ),
        ui.output_text_verbatim(f"param_validation_3_{name_suffix}"),
        #class_="custom-column"
    )
    
def parametros_sin_version_niveles_scorcads():
    return ui.div( ui.row(
                        crear_card_con_input_numeric_2(
                            "par_times", "Submuestras para bootstrap", "times_sub",
                            ui.tags.i(class_="fa fa-question-circle-o",
                                      style="font-size:24px"),
                            global_session_V2.get_json_params_desarrollo(),
                            default_value=25, min_value=0, max_value=2, step=0.01

                        ),
                        crear_card_con_input_numeric_2(
                            "par_cant_reportes", "Cantidad de reportes", "cant_reportes",
                            ui.tags.i(
                                class_="fa fa-question-circle-o", style="font-size:24px"),
                            global_session_V2.get_json_params_desarrollo(),
                            default_value=100, min_value=0, max_value=2, step=0.01
                        ),
                        crear_card_con_input_seleccionador_V3(
                            "par_vars_segmento", "Variables para reportes por Segmento", "vars_segmento",
                            ui.tags.i(
                                class_="fa fa-question-circle-o", style="font-size:24px")
                        ),

                        # style="display: flex; justify-content: space-around; align-items: center;"  # Estilo para mantener todo alineado
                    ),
 
    )
    

