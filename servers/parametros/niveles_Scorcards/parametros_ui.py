from shiny import ui, reactive, render
from clases.global_sessionV2 import *
from clases.global_session import *
from funciones.utils_cargar_json import update_numeric_from_parameters, update_selectize_from_columns_and_json
import pandas as pd


def server_niveles_Scorcards(input, output, session, name_suffix):
    retorne_niveles = reactive.Value(False)

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
    @reactive.event(input.save_modal)
    def valor_min_and_max_ingresado_para_seg():
        min = input.min_value()
        global_session.value_min_for_seg.set(min)
        max = input.max_value()
        global_session.value_max_for_seg.set(max)
        return ui.modal_remove()
        
        