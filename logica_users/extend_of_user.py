from shiny import App, Inputs, Outputs, Session, reactive, ui, render, module
from funciones.nav_panel_User import create_nav_menu_user
from funciones.utils_2 import *
from api import * 
from clases.global_session import global_session
from clases.reactives_name import global_names_reactivos
from funciones.funciones_user import button_remove, create_modal_v2
from funciones.utils_2 import eliminar_archivo, leer_dataset
from logica_users.utils.help_versios import obtener_ultimo_nombre_archivo
from api.db.help_config_db import *
from clases.global_sessionV2 import *
from clases.global_reactives import global_estados
from api.db.sqlite_utils import *
from global_names import base_datos


def extend_user_server(input: Inputs, output: Outputs, session: Session, name):
    
   
    list = reactive.Value(None)
    config_state = reactive.Value({})
    with_values = reactive.Value(False)
    
   
    #EN ESTE ARCHIVO SE MANEJA LA LOGICA DE SELECCIONES SOBRE FILES EN DESARROLLO
    #TAMBIEN SE CREA EL MODAL DE CONFIGURACION
    
    
    @reactive.effect
    @reactive.event(input.files_select)  # Escuchar cambios en el selector
    def project_card_container():
        data_id = input.files_select()  # Captura el ID seleccionado
        global_session.set_id_dataSet(data_id)

        base_datos = 'Modeling_App.db'
        tabla = 'name_files'
        columna_objetivo = 'nombre_archivo'
        columna_filtro = 'id_files'
        nombre_file = obtener_valor_por_id(base_datos, tabla, columna_objetivo, columna_filtro, global_session.get_id_dataSet())
        
        
        actualizar_ultimo_seleccionado(base_datos, 'name_files', 'id_files', data_id)
        ##OBTENGO LOS VALORES ASOCIADOS A LA TABALA
        list = get_records(table='name_files',
            columns=['name_files.id_files', 'name_files.nombre_archivo', 'name_files.fecha_de_carga'],
            join_clause='INNER JOIN version ON name_files.version_id = version.version_id',
            where_clause='version.project_id = ?',
            where_params=(global_session.get_id_proyecto(),))
        
        
        global_names_reactivos.set_name_file_db(nombre_file)
        
        if global_names_reactivos.get_name_file_db() is None:
            global_session_V2.set_dataSet_seleccionado(obtener_ultimo_nombre_archivo(list))
        else:
            global_session_V2.set_dataSet_seleccionado(global_names_reactivos.get_name_file_db())
        #if global_names_reactivos.get_proceso_leer_dataset():
        
        data = leer_dataset(global_session.get_id_user(), global_session.get_id_proyecto(), global_session.get_name_proyecto(), global_names_reactivos.get_name_file_db(), global_session.get_versiones_name(), global_session.get_id_version())
        global_session.set_data_set_reactivo(data)

 
    @output
    @render.ui
    def remove_dataset():
        list.set(get_records(
        table='name_files',
        columns=['id_files', 'nombre_archivo', 'fecha_de_carga'],
        join_clause='INNER JOIN version ON name_files.version_id = version.version_id',
        where_clause='version.version_id = ?',
        where_params=(global_session.get_id_version(),)))
        #name.set(global_names_reactivos.get_name_file_db())
        return button_remove(list.get(), global_session.get_id_dataSet(), "id_files", name)
        
    
    @reactive.Effect
    def boton_para_eliminar_name_data_set():
        eliminar_version_id = f"eliminar_version_{global_session.get_id_dataSet()}_{name}"

        @reactive.Effect
        @reactive.event(input[eliminar_version_id])
        def eliminar_version_id():
            base_datos = 'Modeling_App.db'
            tabla = 'name_files'
            columna_objetivo = 'nombre_archivo'
            columna_filtro = 'id_files'
            nombre_version = obtener_valor_por_id(base_datos, tabla, columna_objetivo, columna_filtro, global_session.get_id_dataSet())
            #nombre_version = obtener_valor_por_id(global_session.get_id_dataSet())
            create_modal_v2(f"Seguro que quieres eliminar el Dataset {nombre_version}?", "Confirmar", "Cancelar", "confirmar_id_borrar_dataset", "cancelar_id_dataSet")
    
    
    @reactive.Effect
    @reactive.event(input["cancelar_id_dataSet"])
    def remove_modal_Dataset():
        ui.modal_remove()   
     
     
    @reactive.Effect
    @reactive.event(input.confirmar_id_borrar_dataset)
    def remove_versiones_de_parametros():
        eliminar_version("name_files", "id_files", global_session.get_id_dataSet())
        datasets_directory = get_datasets_directory_data_set_versiones(global_session.get_id_user(), global_session.get_id_proyecto(), global_session.get_name_proyecto(), global_session.get_versiones_name(), global_session.get_id_version())
        dataset_path = os.path.join(datasets_directory, global_names_reactivos.get_name_file_db())
        eliminar_archivo(dataset_path)
        columnas = ['id_files', 'nombre_archivo']
        tabla = "name_files"
        lista_de_versiones_new = obtener_versiones_por_proyecto(columnas,tabla)

        print(lista_de_versiones_new, "lista_de_versiones_new")
        list.set(lista_de_versiones_new)
        ui.update_select(
            "files_select",
            choices={str(vers['id_files']): vers['nombre_archivo']
                     for vers in lista_de_versiones_new}
        )
        ui.modal_remove()
            
    
    def create_modal():
        current_config = config_state.get()
        return ui.modal(
                ui.tags.div(
                    ui.row(
                        ui.card(
                            ui.column(
                                12,
                                ui.input_numeric(
                                    "number_choice",
                                    "Ingrese un número de columnas para ver en el dataset",
                                    value=current_config["number_choice"],  # Usa el valor actual del estado
                                )
                            ),
                        ),
                        ui.tags.hr(),
                        ui.card(
                            ui.column(
                                12,
                                ui.input_numeric(
                                    "min_value",
                                    "Ingrese el valor minimo para la configuracion de segmentacion",
                                    value=current_config["min_value"]  # Usa el valor actual del estado
                                ),
                                ui.input_numeric(
                                    "max_value",
                                    "Ingrese el valor maximo para la configuracion de segmentacion",
                                    value=current_config["max_value"]  # Usa el valor actual del estado
                                )
                            )
                        ),
                    )
                ),
                title="Configuración de parametros",
                easy_close=True,
                size='l',
                footer=ui.row(
                    ui.column(
                        6,
                        ui.input_action_button("save_modal", "Guardar", class_="btn-primary")
                    ),
                    ui.column(
                        6,
                        ui.input_action_button("close_modal", "Cerrar", class_="btn-secondary")
                    )
                )
            )
        
        
    
    def create_navigation_handler(input_id, screen_name):
        @reactive.Effect
        @reactive.event(input[input_id])
        async def navigate():
            await session.send_custom_message('navigate', screen_name)
            
    

    @reactive.Effect
    def cargar_configuracion_inicial():
            config = obtener_configuracion_por_hash(base_datos, global_session.get_id_user())
            if config:
                valor_min_seg, valor_max_seg, num_select_filas, _ = config.values()
                ui.update_numeric("number_choice",value=num_select_filas)
                ui.update_numeric("min_value",value=valor_min_seg)
                ui.update_numeric("max_value",value=valor_max_seg)
                

        
    @reactive.Effect
    @reactive.event(input["configuracion"])
    def modal():
        #recargar_values_of_config()
        global_estados.value_boolean_for_values_in_config.set(True)
        create_navigation_handler("configuracion","screen_config")
        #ui.modal_show(create_modal())
        
        
    
    @reactive.effect
    def capturar_num_seleccionador_dataSet():
        valor_Defult = "5"
        select_number_data_set = input.number_choice()
        global_estados.set_numero_dataset(select_number_data_set)
        
        
    @reactive.Effect
    @reactive.event(input["close_modal"])
    def cerrar_modal_config():
      create_navigation_handler("close_modal","Screen_User")
        
  
    @reactive.effect
    def up_load_input_dark():
        dark_or_light = input.dark_mode_switch()
        if dark_or_light:
            insertar_configuracion_usuario_con_replace(base_datos, global_session.get_id_user(), value_dark_or_light=dark_or_light)
          
        config = obtener_configuracion_por_hash(base_datos, global_session.get_id_user())
        dark_or_light = config['value_dark_or_light']
        print(dark_or_light, "valor de dark?")
        ui.update_dark_mode(dark_or_light)
        
        
    
    
    @render.text
    def show_data_Set_in_card_user():
        return global_names_reactivos.get_name_file_db() or 'No hay un DataSet seleccionado'
    
    
    
     
  
    
    