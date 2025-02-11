import os
import json
from funciones.utils import crear_card_con_input_seleccionador, crear_card_con_input_numeric_2, crear_card_con_input_seleccionador_V2, crear_card_con_input_seleccionador_V3, crear_card_con_input_seleccionador_V3_sin_multiples_opciones
from shiny import ui
from clases.global_sessionV2 import  *
import pandas as pd


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

def leer_control_json_in_sample(user_id, proyecto_id, name_proyect, id_version, nombre_version, nombre_version_insa, id_version_insa):
    # Obtener la ruta de la carpeta de datasets (o de la versión y proyecto)
    version_folder = get_datasets_directory_json(user_id, proyecto_id, name_proyect, id_version, nombre_version)
    version_insa = f"version_parametros_{id_version_insa}_{nombre_version_insa}"
    full_path = os.path.join(version_folder, version_insa)
    # Verificar que la carpeta de la versión no sea None
    if version_folder is None:
        print(f"No se encontró la carpeta de la versión del proyectooo. {version_folder}")
        return None  # Retornar None si no se encontró la carpeta
    
    # Construir la ruta completa del archivo JSON
    control_json_path = os.path.join(full_path, 'Control de SmartModelStudio.json')
    
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


def get_parameter_value_numeric(param_name, json_params, default=None):
    """
    Obtiene el valor de un parámetro desde una lista de parámetros JSON.

    Args:
        param_name (str): Nombre del parámetro a buscar.
        json_params (list): Lista de diccionarios que contienen parámetros.
        default (optional): Valor predeterminado si no se encuentra el parámetro. Default es None.

    Returns:
        El valor del parámetro si se encuentra, de lo contrario, el valor predeterminado.
    """
    if isinstance(json_params, list):
        # Recorre la lista buscando el parámetro por su nombre
        for param in json_params:
            if param.get("parameter") == param_name:
                return param.get("value", default)
    return default



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

            # Procesa el valor si es un str  con elementos separados por comas
            if isinstance(value, str):
                value = [v.strip() for v in value.split(",")]

            # Actualiza el selectize con los valores seleccionados
            ui.update_selectize(selectize_id, choices=column_names, selected=value)
            
def get_parameter_dataframe(parameter_name, lista):
    """
    Extrae el valor de un parámetro en formato 'data.frame' desde una lista de JSONs y lo convierte en un DataFrame.
    
    :param parameter_name: Nombre del parámetro a buscar en la lista.
    :param lista: Lista de diccionarios JSON que contienen los parámetros.
    :return: DataFrame con los valores extraídos o None si el parámetro no se encuentra o está vacío.
    """
    if lista:
        value = get_parameter_value(parameter_name, lista)
       

        if isinstance(value, dict) and value.keys():  # Caso 1: Formato anterior (diccionario)
            df = pd.DataFrame(value)
            return df
        
        elif isinstance(value, list) and all(isinstance(i, dict) for i in value):  # Caso 2: Lista de diccionarios
            df = pd.DataFrame(value)
            return df
        
        else:
            return None
        
                    
def update_numeric_from_parameters(numeric_params, json_params=None, default_values=None):
    """
    Actualiza las entradas numéricas (`input_numeric`) con valores desde un JSON o un valor predeterminado.

    Args:
        numeric_params (dict): Diccionario donde las claves son IDs de los `input_numeric` y los valores son nombres de parámetros en el JSON.
        json_params (dict, optional): Parámetros cargados desde el JSON. Default es None.
        default_values (dict, optional): Diccionario con valores predeterminados para cada `input_numeric`.
                                          Si no está definido un valor predeterminado para un `input_numeric`,
                                          se usará `0`.
    """
    if default_values is None:
        default_values = {}

    for numeric_id, param_name in numeric_params.items():
        # Obtén el valor predeterminado específico para este numeric_id, o usa 0 como default general
        default_value = default_values.get(numeric_id, 0)

        # Inicializa el valor con el predeterminado
        value = default_value

        # Si hay parámetros en el JSON, busca el valor correspondiente
        if json_params:
            value = get_parameter_value_numeric(param_name, json_params, default=default_value)

            # Si el valor es una lista, selecciona el primer elemento
            if isinstance(value, list) and len(value) > 0:
                value = value[0]
            
            # Verifica que sea numérico, de lo contrario usa el valor predeterminado
            if not isinstance(value, (int, float)):
                value = default_value

        # Actualiza el valor del `input_numeric`
        ui.update_numeric(numeric_id, value=value)



def update_dataframe_from_json(json_data):
    """
    Loads specific values from JSON and converts them to predefined DataFrames.

    Args:
        json_data (list of dict): JSON input as a list of dictionaries.

    Returns:
        dict: A dictionary containing the required DataFrames.
    """
    # Define default structures
    default_niveles_riesgo = pd.DataFrame({
        "Nombre Nivel": ["BajoBajo", "BajoMedio", "BajoAlto", "MedioBajo", "MedioMedio", "Alto"],
        "Regla": ["> 955", "> 930", "> 895", "> 865", "> 750", "<= 750"],
        "Tasa de Malos Máxima": ["3.0%", "6.0%", "9.0%", "15.0%", "18.0%", "100.0%"]
    })

    default_segmentos = pd.DataFrame({
        "Segment": ["Female_Employees", "Male_Employees", "Other", "Other"],
        "Rule": [
            "Gender == 'F' & Job_Type == 'E'",
            "Gender == 'M' & Job_Type == 'E'",
            "Gender == 'F' & (is.na(Job_Type) | Job_Type != 'E')",
            "Gender == 'M' & (is.na(Job_Type) | Job_Type != 'E')"
        ]
    })

    default_rangos = pd.DataFrame({
        "Variables de corte": ["Segmento", "TipoOpe, TipoCmr"]
    })

    # Initialize result with default values
    result = {
        "niveles_riesgo": default_niveles_riesgo,
        "segmentos": default_segmentos,
        "rangos": default_rangos
    }

    # Map parameter names in JSON to result keys
    param_mapping = {
        "par_rango_niveles": "niveles_riesgo",
        "par_rango_segmentos": "segmentos",
        "par_rango_reportes": "rangos"
    }

    for entry in json_data:
        param_name = entry.get("parameter")
        param_type = entry.get("type")
        value = entry.get("value")

        # Process only parameters that are mapped and of type "data.frame"
        if param_name in param_mapping and param_type == "data.frame":
            try:
                # Check if value is empty or invalid and replace with default
                if isinstance(value, dict) and not value:
                    df = result[param_mapping[param_name]]  # Use default
                elif isinstance(value, list) and all(isinstance(row, dict) for row in value):
                    df = pd.DataFrame(value)  # Convert list of dicts to DataFrame
                else:
                    df = pd.DataFrame()  # Fallback to empty DataFrame

                # Update the result with the loaded or default DataFrame
                result[param_mapping[param_name]] = df
            except Exception as e:
                print(f"Error processing parameter {param_name}: {e}")

    return result




def parametros_sin_version(name_suffix):
    return ui.div(
        ui.output_ui(f"acordeon_columnas_{name_suffix}"),
        ui.card(
            ui.row(
                # Fila 1
                crear_card_con_input_seleccionador(
                    "par_ids",
                    "Columnas identificadora:",
                    "help_columnas_id",
                    ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px")
                ),
                crear_card_con_input_numeric_2(
                    f"par_split",
                    "Training and Testing",
                    "help_training_testing",
                    ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"),
                    default_value=0.7,
                    min_value=0.7,
                    max_value=2,
                    step=0.01
                ),
                crear_card_con_input_seleccionador_V3_sin_multiples_opciones("par_target", "Columna Target", "help_target_col", 
                                                        ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"),
                                                        ),


                # Fila 2
                crear_card_con_input_seleccionador(
                    f"cols_forzadas_a_predictoras",
                    "Variables forzadas a variables candidatas",
                    "help_vars_forzadas",
                    ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px")
                ),
                crear_card_con_input_seleccionador(
                    f"cols_forzadas_a_cat",
                    "Columnas forzadas a categorías",
                    "help_cols_forzadas_a_cat",
                    ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px")
                ),
                crear_card_con_input_seleccionador(
                    f"par_var_grupo",
                    "Grupos para evaluar las candidatas",
                    "help_par_var_grupo",
                    ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px")
                ),

                # Fila 3
                crear_card_con_input_seleccionador(
                    "cols_nulos_adic",
                    "Lista de variables y códigos de nulos",
                    "help_nulos_adic",
                    ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px")
                ),
                crear_card_con_input_numeric_2(
                    f"par_cor_show",
                    "Mostrar variables por alta correlación:",
                    "help_par_cor_show",
                    ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"),
                    default_value=0.9,
                    min_value=0.9,
                    max_value=2,
                    step=0.01
                ),
                crear_card_con_input_numeric_2(
                    f"par_iv",
                    "Descartar variables por bajo IV",
                    "help_iv",
                    ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"),
                    default_value=3,
                    min_value=3,
                    max_value=10,
                    step=0.01
                ),

                # Fila 4
                crear_card_con_input_seleccionador_V2(
                    f"cols_no_predictoras",
                    "Columnas excluidas del modelo",
                    "help_cols_no_predictoras",
                    ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px")
                ),
                crear_card_con_input_numeric_2(
                    f"par_cor",
                    "Descartar variables por alta correlación",
                    "help_par_cor",
                    ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"),
                    default_value=0.9,
                    min_value=0.9,
                    max_value=2,
                    step=0.01
                ),
                crear_card_con_input_numeric_2(
                    f"par_minpts1",
                    "Casos mínimos de bin de primera etapa",
                    "help_minpts",
                    ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"),
                    default_value=200,
                    min_value=200,
                    max_value=1000,
                    step=0.01
                )
            ),
            ui.output_ui(f"error_{name_suffix}"),
        ),
        ui.output_text_verbatim(f"param_validation_3_{name_suffix}")
    )
    
    
def actualizar_json(file1, file2, output_file):
    """
    Combina dos archivos JSON en uno, llenando claves faltantes, 
    y guarda el resultado en un nuevo archivo.

    :param file1: Ruta al primer archivo JSON.
    :param file2: Ruta al segundo archivo JSON.
    :param output_file: Ruta donde se guardará el archivo combinado.
    """
    # Leer los archivos JSON
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)

    # Combinar las claves
    combined = {key: data1.get(key, data2.get(key)) for key in set(data1) | set(data2)}

    # Guardar el JSON combinado
    with open(output_file, 'w') as outfile:
        json.dump(combined, outfile, indent=4)

    print(f"Archivo combinado creado: {output_file}")