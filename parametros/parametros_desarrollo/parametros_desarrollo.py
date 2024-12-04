from shiny import App, reactive, render, ui
from funciones.utils import validar_columnas, validate_par_iv, process_target_col1, create_modal_parametros, id_buttons
from clases.loadJson import LoadJson
from global_var import global_data_loader_manager
import pandas as pd 
from funciones.utils_2 import cambiarAstring, trans_nulos_adic, validar_proyecto, mostrar_error
from clases.global_session import global_session
from clases.global_reactives import global_estados
from clases.class_cargar_datos import CargarDatos
from clases.global_sessionV2 import *
from funciones.utils_cargar_json import get_parameter_value, update_selectize_from_columns_and_json, update_numeric_from_parameters
from funciones.utils import  crear_card_con_input_numeric_2, crear_card_con_input_seleccionador_V2, crear_card_con_input_seleccionador_V3


def server_parametros_desarrollo(input, output, session, name_suffix):
    # Obtener el DataLoader correspondiente basado en name_suffix, ya que necesita un key la clase dataloader
    data_loader = global_data_loader_manager.get_loader(name_suffix)
    
    def user_session():
        @reactive.Effect
        def obtener_user() -> str:
            if global_session.proceso.get():
                state = global_session.session_state.get()
                if state["is_logged_in"]:
                    user_id = state["id"]
                    return user_id
        
    
    
         # Definir las unciones de transformación para cada input
    transformaciones = {
        'par_ids': cambiarAstring,
        'par_target': cambiarAstring,
        'cols_forzadas_a_predictoras': cambiarAstring,
        'par_var_grupo': cambiarAstring,
        'cols_nulos_adic': trans_nulos_adic,
        'cols_forzadas_a_cat': cambiarAstring,
        'cols_no_predictoras': cambiarAstring
        
    }

    
    
    def create_navigation_handler(input_id, screen_name, valid):
        @reactive.Effect
        @reactive.event(input[input_id])
        async def navigate():
            if valid.get():
                await session.send_custom_message('navigate', screen_name)
    
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
            print("pase, aca??")
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

            json_params = global_session_V2.get_json_params_desarrollo()

        # Llama a la función genérica para actualizar los selectores
            update_selectize_from_columns_and_json(column_names, selectize_params, json_params) 
                
        
    @reactive.effect
    def create_parametros_from_json():
        @output
        @render.ui
        def parametros_desarrolo():
            print("ESTOY ANTES DE RETORNAR")
            if global_session_V2.get_json_params_desarrollo():
                value_par_id = get_parameter_value('par_ids', global_session_V2.get_json_params_desarrollo())
                value_par_id = [value_par_id]
                return ui.div(
                    ui.output_ui(f"acordeon_columnas_{name_suffix}"),
                    ui.card(
                        ui.row(
                            # Fila 1
                            crear_card_con_input_seleccionador_V3("par_ids", "Columnas identificadora:", "help_columnas_id", 
                                                            ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"),
                                                            ),
                            
                            crear_card_con_input_numeric_2(
                            input_id="par_split",
                            input_label="Training and Testing",
                            action_link_id="help_training_testing",
                            icon=ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"),
                            min_value=0,
                            max_value=2,
                            step=0.01
                            ),
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
                            
                           crear_card_con_input_numeric_2(
                            input_id="par_cor_show",
                            input_label="Mostrar variables por alta correlación:",
                            action_link_id="help_par_cor_show",
                            icon=ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"),
                            min_value=0,
                            max_value=1,
                            step=0.01
                        ), 
                            crear_card_con_input_numeric_2(
                            input_id="par_iv",
                            input_label="Límite para descartar variables por bajo IV",
                            action_link_id="help_iv",
                            icon=ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"),
                            min_value=0.5,
                            max_value=10,
                            step=0.1
                        ),
                            # Fila 4
                            crear_card_con_input_seleccionador_V3(f"cols_no_predictoras", "Columnas excluidas del modelo", 
                                                                "help_cols_no_predictoras", ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"),
                                                                ),
                            
                            crear_card_con_input_numeric_2(
                            input_id="par_cor",
                            input_label="Descartar variables por alta correlación",
                            action_link_id="help_par_cor",
                            icon=ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"),
                            min_value=0.5,
                            max_value=10,
                            step=0.1
                        ),
                            crear_card_con_input_numeric_2(
                        input_id="par_minpts1",
                        input_label="Casos mínimos de bin de primera etapa",
                        action_link_id="help_minpts",
                        icon=ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"),
                        min_value=0.5,
                        max_value=10,
                        step=0.1
                    ),
                        ),
                        ui.output_ui(f"error_{name_suffix}"),
                    ),
                    
                    ui.output_text_verbatim(f"param_validation_3_{name_suffix}"),
                    
                    global_session_V2.set_retornado(True)
                )
            else:
                    
                global_session_V2.set_retornado(True),
                #return parametros_sin_version(name_suffix)


                    
    @reactive.Effect
    def up_date_inputs_numerics():
        numeric_params = {
            "par_split": "par_split",
            "par_cor_show": "par_cor_show",
            "par_iv": "par_iv",
            "par_cor": "par_cor",
            "par_minpts1": "par_minpts1"
        }
        
        json_params = global_session_V2.get_json_params_desarrollo()
        
        default_values = {
            "par_split": 0.7,
            "par_cor_show": 0.8,
            "par_iv": 3.0,
            "par_cor": 0.9,
            "par_minpts1": 0.5
        }

        update_numeric_from_parameters(numeric_params, json_params, default_values)
  

            
            
        
    
        
    