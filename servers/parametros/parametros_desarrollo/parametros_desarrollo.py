from shiny import App, reactive, render, ui
from funciones.utils import  create_modal_parametros, id_buttons
from clases.global_session import global_session
from funciones.help_parametros.valid_columns import *
from funciones.utils_2 import *
from clases.global_sessionV2 import *
from funciones.help_parametros import *
from funciones.utils import create_modal_parametros, id_buttons_desa
from funciones.utils_cargar_json import get_parameter_value, update_selectize_from_columns_and_json, update_numeric_from_parameters, parametros_sin_version
from funciones.utils import  crear_card_con_input_numeric_2, crear_card_con_input_seleccionador_V2, crear_card_con_input_seleccionador_V3, crear_card_con_input_seleccionador_V3_sin_multiples_opciones


def server_parametros_desarrollo(input, output, session, name_suffix):
    # Obtener el DataLoader correspondiente basado en name_suffix, ya que necesita un key la clase dataloader
    count = reactive.value(0)
    no_version =  reactive.Value(False)
    selected_value = reactive.Value(None)
    select_value_operator = reactive.Value(None)
    selected_value_num = reactive.Value(None)
    step3 =  reactive.Value(False)
    step2 = reactive.Value(False)
    
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
                column_target = get_binary_columns(df)
            else:
                column_names = []
                column_target = []

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
            
            selectize_params_only_target = {
                "par_target": "par_target",  
            }
            
            
            json_params = global_session_V2.get_json_params_desarrollo()

    
            update_selectize_from_columns_and_json(column_names, selectize_params, json_params)
            update_selectize_from_columns_and_json(column_target, selectize_params_only_target, json_params)
           
            
            
    @reactive.Effect
    @reactive.event(input["cols_nulos_adic"])
    def change():
        value_cols_nulos_adic = input[f'cols_nulos_adic']()
        last_value = value_cols_nulos_adic
        value_cols_nulos_adic = cambiarAstring(value_cols_nulos_adic)
        if value_cols_nulos_adic != "=" and value_cols_nulos_adic != "!=":
            value_select = value_cols_nulos_adic
            selected_value.set(value_select)
        
        fixed_choices = ["=", "!="]
        if selected_value.get() not in fixed_choices:
            
            if last_value:  # Si last_value tiene un valor
                last_value = get_equal_from_tuple(last_value)  # Procesa la tupla
                # Compara explícitamente last_value con fixed_choices
                if last_value in fixed_choices:
                    select_value_operator.set(last_value)
                        
            dynamic_operator = fixed_choices + [selected_value.get()]
            ui.update_select("cols_nulos_adic", choices=dynamic_operator, selected=selected_value.get())
        
        if select_value_operator.get() in fixed_choices:
            operator_list = ['0', '1', 'Null']
            # Concatenamos las listas correctamente
            dynamic_choices = dynamic_operator + operator_list + [select_value_operator.get()]
   
            if select_value_operator.get() not in operator_list:
                selected_value_num.set(value_cols_nulos_adic)
                
            # Actualizamos el selector
            ui.update_select("cols_nulos_adic", choices=dynamic_choices, selected=selected_value.get())
            step3.set(True)
            
        
        
        
      
            
    processed_ids = set()

    def create_modals(id_buttons_desa):
        for id_button in id_buttons_desa:
            if id_button in processed_ids:
                continue  # Saltar IDs ya procesados

            processed_ids.add(id_button)  # Registrar como procesado

            @reactive.Effect
            @reactive.event(input[id_button])
            def monitor_clicks(id_button=id_button):
                count.set(count() + 1)
                if count.get() > 0:
                    print(id_button, count.get())
                    modal = create_modal_parametros(id_button)
                    ui.modal_show(modal)


                
    
    @output
    @render.ui
    def parametros_desarrolo():
        if global_session_V2.get_json_params_desarrollo():
            no_version.set(False),
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
                        default_value=0.7,
                        min_value=0,
                        max_value=2,
                        step=1,
                        ),
                        crear_card_con_input_seleccionador_V3_sin_multiples_opciones("par_target", "Columna Target", "help_target_col", 
                                                        ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"),
                                                        ),

                        # Fila 2
                        crear_card_con_input_seleccionador_V2(f"cols_forzadas_a_predictoras", "Variables forzadas a variables candidatas", 
                                                        "help_vars_forzadas", ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"),),
                        
                        crear_card_con_input_seleccionador_V3(f"cols_forzadas_a_cat", "Columnas forzadas a categorías", 
                                                        "help_cols_forzadas_a_cat", ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"),
                                                        ),
                        
                        crear_card_con_input_seleccionador_V3(f"par_var_grupo", "Grupos para evaluar las candidatas", 
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
                        default_value=0.9,
                        min_value=0,
                        max_value=0.9,
                        step=0.01
                    ), 
                        crear_card_con_input_numeric_2(
                        input_id="par_iv",
                        input_label="Descartar variables por bajo IV",
                        action_link_id="help_iv",
                        icon=ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"),
                        default_value=10,
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
                        default_value=0.5,
                        min_value=0.5,
                        max_value=10,
                        step=0.1
                    ),
                        crear_card_con_input_numeric_2(
                    input_id="par_minpts1",
                    input_label="Casos mínimos de bin de primera etapa",
                    action_link_id="help_minpts",
                    icon=ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"),
                    default_value=200,
                    min_value=200,
                    max_value=10,
                    step=1,
                ),
                    ),
                    ui.output_ui(f"error_{name_suffix}"),
                ),
                
                ui.output_text_verbatim(f"param_validation_3_{name_suffix}"),
                create_modals(id_buttons_desa),
                global_session_V2.set_retornado(True),
                
            )
        else:
            
            global_session_V2.set_retornado(True),
            no_version.set(True),
            

    @output
    @render.ui
    def return_params_sin_version():
        if no_version.get():
            return parametros_sin_version(name_suffix)
            
     

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
            "par_cor_show": 0.9,
            "par_iv": 3.0,
            "par_cor": 0.9,
            "par_minpts1":200
        }

        update_numeric_from_parameters(numeric_params, json_params, default_values)
  

            
            
   