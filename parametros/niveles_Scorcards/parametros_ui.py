from shiny import ui, reactive, render
from clases.global_sessionV2 import *
from clases.global_session import *
from funciones.utils import crear_card_con_input_numeric, crear_card_con_input_seleccionador_V3, crear_card_con_input_numeric_2
from funciones.utils_cargar_json import parametros_sin_version_niveles_scorcads, update_selectize_from_columns_and_json
import pandas as pd


def server_niveles_Scorcards(input, output, session, name_suffix):
    retorne_niveles = reactive.Value(False)
    
    
    @reactive.effect
    @reactive.event(input.times_sub)  # Escucha el evento de cambio del input 'times_sub'
    def obtener_valor():
        valor = input.times_sub()  # Accede al valor actual del input 'times_sub'
        print(f"El valor de times_sub es: {valor}")
        return valor  # Puedes devolver el valor o usarlo para algo más


    @reactive.effect
    def crear_parametros_validacion_scorcads():
        @output
        @render.ui
        def parametros_json_niveles():
            if global_session_V2.get_json_params_desarrollo():
                print("estoy pasando??????")
                return ui.div(
                    ui.row(
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
                    global_session_V2.set_retorne_niveles(True)
                )
            else:
                print("estoy, aca")
                global_session_V2.set_retorne_niveles(True)
                return parametros_sin_version_niveles_scorcads()
            
            

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