from shiny import App, reactive, render, ui
from global_var import global_data_loader_manager
import pandas as pd 
from funciones.utils_2 import  mostrar_error
from clases.global_session import global_session

from clases.global_sessionV2 import *
from funciones.utils_cargar_json import get_parameter_value, parametros_sin_version
from funciones.utils import  crear_card_con_input_numeric_2, crear_card_con_input_seleccionador_V2, crear_card_con_input_seleccionador_V3


def server_parametros_desarrollo(input, output, session, name_suffix):
    # Obtener el DataLoader correspondiente basado en name_suffix, ya que necesita un key la clase dataloader
    data_loader = global_data_loader_manager.get_loader(name_suffix)
    mensaje = reactive.Value("")  # Reactive value para el mensaje de error
    mensjae_error_proyecto = reactive.Value("")
    no_error = reactive.Value(True)
    value_par_id = reactive.Value([])
    

    @output
    @render.text
    def error_proyecto():
        return mostrar_error(mensjae_error_proyecto.get())
          
               
    
   
    
    ##ES IMPORTANTE USAR ESTA FUNCION Y DECLARAR EL PARAMETO QUE LE CORRESPONDE, PARA ACTUALIZAR EL UI DE SELECCIONADOR
    # ESTO FUNCIONA ASI: ACTUALIZA EL VALOR UNA VEZ DELCARADO PARA QUE RECONOZCA LAS COLUMNAS
    ## SI DECLARAMOS UN NUEVO PARAMETRO QUE SEA SELECCIONADOR NO VA A FUNCION SI NO LO ADJUTAMOS DEBAJO EN EL  ui.update_selectize
    @reactive.Effect
    def update_column_choices():
        # Verifica si el retorno está listo
        if global_session_V2.get_retornado():
            # Carga el DataFrame y obtiene sus columnas
            df = global_session.get_data_set_reactivo()  # Asegúrate de obtener el DataFrame del cargador de datos
            if isinstance(df, pd.DataFrame) and not df.empty:
                column_names = df.columns.tolist()
            else:
                column_names = []

            # Define un diccionario para mapear los IDs de selectize con los nombres de parámetros en el JSON
            selectize_params = {
                "par_ids": "par_ids",
                "cols_forzadas_a_cat": "cols_forzadas_a_cat",
                "par_var_grupo": "par_var_grupo",
                "par_target": "par_target",
                "cols_no_predictoras": "cols_no_predictoras",
                "cols_nulos_adic": "cols_nulos_adic",
                "cols_forzadas_a_predictoras": "cols_forzadas_a_predictoras",
                "par_vars_segmento": "par_vars_segmento",
            }

            # Si hay parámetros en el JSON, actualiza los valores seleccionados
            if global_session_V2.get_json_params_desarrollo():
                json_params = global_session_V2.get_json_params_desarrollo()
                for selectize_id, param_name in selectize_params.items():
                    # Obtén el valor del parámetro
                    print()
                    value = get_parameter_value(param_name, json_params)
                    
                    # Procesa el valor si es una cadena con elementos separados por comas
                    if isinstance(value, str):
                        value = [v.strip() for v in value.split(",")]
                    
                    # Actualiza el selectize con los valores seleccionados
                    #print(selectize_id)
                    ui.update_selectize(selectize_id, choices=column_names, selected=value)        
                
        
    @reactive.effect
    def create_parametros_from_json():
        @output
        @render.ui
        def parametros_desarrolo():
            if global_session_V2.get_json_params_desarrollo():
                return ui.div(
                    ui.output_ui(f"acordeon_columnas_{name_suffix}"),
                    ui.card(
                        ui.row(
                            # Fila 1
                            crear_card_con_input_seleccionador_V3("par_ids", "Columnas identificadora:", "help_columnas_id", 
                                                            ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"),
                                                            ),
                            
                            crear_card_con_input_numeric_2(f"par_split", "Training and Testing", "help_training_testing", 
                                                        ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"), 
                                                        global_session_V2.get_json_params_desarrollo(), default_value=0, min_value=0, max_value=2, step=0.01),
                            
                            crear_card_con_input_seleccionador_V3("par_target", "Columna Target", "help_target_col", 
                                                            ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"),
                                                            ),

                            # Fila 2
                            crear_card_con_input_seleccionador_V2(f"cols_forzadas_a_predictoras", "Variables forzadas a variables candidatas", 
                                                            "help_vars_forzadas", ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"),),
                            
                            crear_card_con_input_seleccionador_V3(f"cols_forzadas_a_cat", "Columnas forzadas a categorías", 
                                                            "help_cols_forzadas_a_cat", ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"),
                                                            ),
                            
                            crear_card_con_input_seleccionador_V3(f"par_var_grupo", "Define grupos para evaluar las candidatas", 
                                                            "help_par_var_grupo", ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"),
                                                            ),

                            # Fila 3
                            crear_card_con_input_seleccionador_V3("cols_nulos_adic", "Lista de variables y códigos de nulos", 
                                                                "help_nulos_adic", ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"),
                                                                ),
                            
                            crear_card_con_input_numeric_2(f"par_cor_show", "Mostrar variables por alta correlación:", "help_par_cor_show", 
                                                        ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"), 
                                                        global_session_V2.get_json_params_desarrollo(), default_value=0, min_value=0, max_value=1, step=0.01),
                            
                            crear_card_con_input_numeric_2(f"par_iv", "Límite para descartar variables por bajo IV", "help_iv", 
                                                        ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"), 
                                                        global_session_V2.get_json_params_desarrollo(), default_value=3, min_value=0.5, max_value=10, step=0.1),

                            # Fila 4
                            crear_card_con_input_seleccionador_V3(f"cols_no_predictoras", "Columnas excluidas del modelo", 
                                                                "help_cols_no_predictoras", ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"),
                                                                ),
                            
                            crear_card_con_input_numeric_2(f"par_cor", "Descartar variables por alta correlación", "help_par_cor", 
                                                        ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"), 
                                                        global_session_V2.get_json_params_desarrollo(), default_value=3, min_value=0.5, max_value=10, step=0.1),
                            
                            crear_card_con_input_numeric_2(f"par_minpts1", "Casos mínimos de bin de primera etapa", "help_minpts", 
                                                        ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"), 
                                                        global_session_V2.get_json_params_desarrollo(), default_value=3, min_value=0.5, max_value=10, step=0.1)
                        ),
                        ui.output_ui(f"error_{name_suffix}"),
                    ),
                    
                    ui.output_text_verbatim(f"param_validation_3_{name_suffix}"),
                    
                    global_session_V2.set_retornado(True)
                )
            else:
                  return parametros_sin_version(name_suffix)