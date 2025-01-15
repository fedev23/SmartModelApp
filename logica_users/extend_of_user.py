from shiny import App, Inputs, Outputs, Session, reactive, ui, render, module
from clases.global_modelo import global_desarollo
from funciones_modelo.help_models import *
from funciones.utils_2 import *
from api import * 
from logica_users.utils.help_versios import mapear_valor_a_clave
from clases.global_session import global_session
from clases.reactives_name import global_names_reactivos
from funciones.funciones_user import button_remove, create_modal_v2
from funciones.utils_2 import eliminar_archivo, leer_dataset
from logica_users.utils.help_versios import obtener_ultimo_nombre_archivo
from api.db.help_config_db import *
from funciones_modelo.warning_model import create_modal_warning_exist_model, validar_existencia_modelo_por_dinamica_de_app
from clases.global_sessionV2 import *
from clases.global_reactives import global_estados
from api.db.sqlite_utils import *
from global_names import base_datos
from clases.global_sessionV3 import *
from logica_users.utils.manejo_session import manejo_de_ultimo_seleccionado

def extend_user_server(input: Inputs, output: Outputs, session: Session, name):
    
   
    lista_reactiva = reactive.Value(None)
    config_state = reactive.Value({})
    click = reactive.Value(0)
    pase_para_cambiar_file = reactive.Value(False)
    initialized = reactive.Value(False)
    
   
    #EN ESTE ARCHIVO SE MANEJA LA LOGICA DE SELECCIONES SOBRE FILES EN DESARROLLO
    #TAMBIEN SE CREA EL MODAL DE CONFIGURACION
    
    
    @reactive.Effect
    @reactive.event(input.files_select)  # Escuchar cambios en el selector de archivos
    def project_card_container():
        # Verificar inicialización para evitar ejecución al cargar la aplicación
        if not initialized():
            initialized.set(True)
            return 
        
        if global_session_V2.boolean_for_change_file.get():
            data = leer_dataset(
            global_session.get_id_user(),
            global_session.get_id_proyecto(),
            global_session.get_name_proyecto(),
            global_names_reactivos.get_name_file_db(),
            global_session.get_versiones_name(),
            global_session.get_id_version()
        )   
            selected_key = mapear_valor_a_clave(global_session_V2.get_dataSet_seleccionado(), global_session_V2.lista_nombre_archivos_por_version.get())
            ui.update_select("files_select", selected=selected_key if selected_key else next(iter(global_session_V2.lista_nombre_archivos_por_version.get()), ""))
            global_session.set_data_set_reactivo(data)
            pase_para_cambiar_file.set(True)
            return 
         
        data_id = input.files_select()  # Captura el ID del archivo seleccionado
        # Actualizar el ID del dataset en la sesión global
        global_session.set_id_dataSet(data_id)

        # Obtener el nombre del archivo desde la base de datos
        tabla = 'name_files'
        columna_objetivo = 'nombre_archivo'
        columna_filtro = 'id_files'
        nombre_file = obtener_valor_por_id(base_datos, tabla, columna_objetivo, columna_filtro, data_id)

        actualizar_ultimo_seleccionado(base_datos, 'name_files', 'id_files', data_id)

        # Configurar el nombre del archivo en reactivos globales
        if nombre_file:
            global_names_reactivos.set_name_file_db(nombre_file)
        else:
            global_session_V2.set_dataSet_seleccionado(obtener_ultimo_nombre_archivo(lista_reactiva.get()))

        # Leer el dataset
        name_dat = input[f'files_select']()
        name_dat = cambiarAstring(name_dat)
        global_names_reactivos.set_name_file_db(nombre_file)
        data = leer_dataset(
            global_session.get_id_user(),
            global_session.get_id_proyecto(),
            global_session.get_name_proyecto(),
            global_names_reactivos.get_name_file_db(),
            global_session.get_versiones_name(),
            global_session.get_id_version()
        )
        click.set(click() + 1)
        global_session_V2.count_global.set(global_session_V2.count_global() + 1)
        global_session.set_data_set_reactivo(data)
        # Validar si el archivo puede cambiar


    @reactive.effect
    def monitoring_change_file():
            if global_session_V2.count_global.get() >= 1 or pase_para_cambiar_file.get():
                base_datos = 'Modeling_App.db'
                print("estoy aca, en monitoring")

                global_session_V2.count_global.set(0)  # Reiniciar el contador para evitar ejecuciones repetidas
                
                print("estoy aca, en monitoring, parte dos")
                # Validar si existe un modelo generado
                modelo_existente = validar_existencia_modelo_por_dinamica_de_app(
                    modelo_boolean_value=global_desarollo.pisar_el_modelo_actual.get(),
                    base_datos=base_datos,
                    version_id=global_session.get_id_version()
                )

                if modelo_existente:
                    # Mostrar el modal de advertencia si ya existe un modelo
                    ui.modal_show(
                        create_modal_warning_exist_model(
                            name=global_desarollo.nombre,
                            nombre_version=global_session_V3.name_version_original.get()
                        )
                    )
                    # Bloquear cambios en el archivo
                    global_session_V2.boolean_for_change_file.set(True)
                else:
                    # Permitir el cambio de archivo
                    global_session_V2.boolean_for_change_file.set(False)

    @output
    @render.ui
    def remove_dataset():
        lista_reactiva.set(get_records(
            table='name_files',
            columns=['id_files', 'nombre_archivo', 'fecha_de_carga'],
            where_clause='project_id = ?',  # Cambiar la cláusula a usar project_id directamente
            where_params=(global_session.get_id_proyecto(),)
        ))
        #name.set(global_names_reactivos.get_name_file_db())
        print(lista_reactiva.get(), "viendo lista")
        print(global_session.get_id_dataSet(), "id data?")
        return button_remove(lista_reactiva.get(), global_session.get_id_dataSet(), "id_files", name)
        
    
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
        datasets_directory = get_datasets_directory(global_session.get_id_user(), global_session.get_id_proyecto(), global_session.get_name_proyecto())
        dataset_path = os.path.join(datasets_directory, global_names_reactivos.get_name_file_db())
        eliminar_archivo(dataset_path)
        lista_de_versiones_new = get_records(
            table='name_files',
            columns=['id_files', 'nombre_archivo', 'fecha_de_carga'],
            where_clause='project_id = ?',  # Cambiar la cláusula a usar project_id directamente
            where_params=(global_session.get_id_proyecto(),)
        )
        print(lista_de_versiones_new, "lista_de_versiones_new")
        lista_reactiva.set(lista_de_versiones_new)
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
            
    
    def load_config():
        @reactive.Effect
        def cargar_configuracion_inicial():
                config = obtener_configuracion_por_hash(base_datos, global_session.get_id_user())
                if config:
                    valor_min_seg, valor_max_seg, num_select_filas, value_dark_or_light = config.values()
                    ui.update_numeric("number_choice",value=num_select_filas)
                    ui.update_numeric("min_value",value=valor_min_seg)
                    ui.update_numeric("max_value",value=valor_max_seg)
                    print(value_dark_or_light, "value dark?")
                    ui.update_dark_mode(value_dark_or_light)
                    
    load_config()
        
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
            print("entrando a dark or light")
            insertar_configuracion_usuario_con_replace(base_datos, global_session.get_id_user(), value_dark_or_light=dark_or_light)
        
        
    
    
    @render.text
    def show_data_Set_in_card_user():
        return global_names_reactivos.get_name_file_db() or 'No hay un DataSet seleccionado'
    
    
    
     
  
    
    