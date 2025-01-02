from shiny import ui, reactive, render
from clases.global_sessionV2 import *
from clases.global_session import *
from funciones.utils_cargar_json import update_numeric_from_parameters, update_selectize_from_columns_and_json
import pandas as pd
from clases.reactives_name import global_names_reactivos
from funciones.help_parametros.valid_columns import *
from api import *
from clases.global_session import global_session
from clases.global_sessionV2 import *
from funciones.utils_2 import *
from logica_users.utils.help_versios import obtener_opciones_versiones, obtener_ultimo_id_version, eliminar_carpeta, mapear_valor_a_clave
from funciones.utils_cargar_json import leer_control_json
from api.db.sqlite_utils import *
from api.db.sqlite_utils import *
from funciones_modelo.global_estados_model import global_session_modelos
from funciones_modelo import help_models 
from funciones.funciones_user import create_modal_versiones, show_selected_project_card, create_modal_eliminar_bd, create_modal_v2, button_remove_version


def server_niveles_Scorcards(input, output, session, name_suffix):
    count = reactive.value(0)
    count_add_files = reactive.Value(0)
    global_names_reactivos.name_validacion_in_sample_set(name_suffix)

    
    @reactive.Effect
    def update_column_choices():
        # Carga el DataFrame y obtiene sus columnas
        df = global_session.get_data_set_reactivo()  # Asegúrate de obtener el DataFrame del cargador de datos
        if isinstance(df, pd.DataFrame) and not df.empty:
            column_names = df.columns.tolist()
        else:
            column_names = []

        # Define un diccionario para mapear los IDs de selectize con los nombres de parámetros en el JSON
        
        ui.update_selectize("par_vars_segmento", choices=column_names)
        selectize_params = {
            "par_vars_segmento": "par_vars_segmento",
        }

        # Obtén los parámetros del JSON si están disponibles
        json_params = global_session_V2.get_json_params_desarrollo()

        # Llama a la función genérica para actualizar los selectores
        update_selectize_from_columns_and_json(column_names, selectize_params, json_params)
        
    
    @reactive.Effect
    def up_date_inputs_numerics():
        numeric_params = {
        "par_times": "par_times",
        "par_cant_reportes": "par_cant_reportes",
        "par_times": "par_times"
        }
        
        json_params = global_session_V2.get_json_params_desarrollo()
        
        default_values = {
        "par_times": 25,
        "par_cant_reportes": 100, # Valor predeterminado para numeric_input_3
        }

        update_numeric_from_parameters(numeric_params, json_params, default_values)

    
    
    
    @reactive.Effect
    @reactive.event(input.add_fila)
    def evento_agregar_nueva_fila():
        count_add_files.set(count() + 1)
        column_names = get_categorical_columns_with_unique_values_range(global_session.get_data_set_reactivo(), min_unique=global_session.value_min_for_seg.get(), max_unique=global_session.value_max_for_seg.get())
        #column_names = df.columns.tolist()
        ui.update_selectize("agregar_filas", choices=column_names)
    
   
    
    