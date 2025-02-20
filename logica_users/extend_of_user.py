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
from funciones_modelo.warning_model import create_modal_warning_exist_model, obtener_ultimo_id_DataSet_modelo_Desa, tiene_modelo_generado, create_modal_generic, obtener_nombre_dataset, verificar_estado_modelo
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
    modelo_existe_reactivo = reactive.Value(False)
    hay_modelo = reactive.Value(False)
    contador_for_files = reactive.Value(0)
    
    
    
   
    #EN ESTE ARCHIVO SE MANEJA LA LOGICA DE SELECCIONES SOBRE FILES EN DESARROLLO
    #TAMBIEN SE CREA EL MODAL DE CONFIGURACION
    
    ##HACER LO DEL DICCIONARIO
#delete_button_effects = {}  # 🔹 (Podría eliminarse si no se usa en otro lado)
    contador_for_files = reactive.Value(0)  # Contador único para identificar los modales

    @reactive.Effect
    @reactive.event(input.files_select)  # Escuchar cambios en el selector de archivos
    def project_card_container():
        # Verificar inicialización para evitar ejecución al cargar la aplicación
        if not initialized():
            initialized.set(True)
            return 
        
        global_session_V2.count_global.set(global_session_V2.count_global() + 1)        
        if global_session_V2.count_global.get() > 1:
            
            id_data_desa = obtener_ultimo_id_DataSet_modelo_Desa(db_path=base_datos, version_id=global_session.get_id_version())
            model_ok = verificar_estado_modelo(base_datos, version_id=global_session.get_id_version(), dataset_id=global_session.get_id_dataSet())
            
            if model_ok:
                nombre_dataSet_con_modelo = obtener_nombre_dataset(global_session.get_id_version())
                global_names_reactivos.set_name_file_db(nombre_dataSet_con_modelo)
                
            if model_ok:
                if id_data_desa is not None and id_data_desa != global_session.get_id_dataSet():
                    # Aumentamos el contador para crear un ID único cada vez
                    reactive.invalidate_later(2)
                    
                    
                    contador_for_files.set(contador_for_files() + 1)

                    global_session_V3.modelo_existe.set(True)
                    modelo_existe_reactivo.set(True)

                    # Mostramos el modal
                    ui.modal_show(
                        create_modal_warning_exist_model(
                            name=global_desarollo.nombre,
                            nombre_version=global_session_V3.name_version_original.get(),  # ID único
                        )
                    )

                    # Procesamos el dataset
                    data = leer_dataset(
                        global_session.get_id_user(),
                        global_session.get_id_proyecto(),
                        global_session.get_name_proyecto(),
                        global_names_reactivos.get_name_file_db(),
                        global_session.get_versiones_name(),
                        global_session.get_id_version()
                    )   

                    # Seleccionamos el dataset correspondiente
                    selected_key = mapear_valor_a_clave(
                        global_session_V2.get_dataSet_seleccionado(),
                        global_session_V2.lista_nombre_archivos_por_version.get()
                    )
                    ui.update_select(
                        "files_select",
                        selected=selected_key if selected_key else next(iter(global_session_V2.lista_nombre_archivos_por_version.get()), "")
                    )

                    # Actualizamos las variables globales
                    global_session.set_data_set_reactivo(data)
                    hay_modelo.set(True)
                    pase_para_cambiar_file.set(True)
                    global_session_V2.count_global.set(1)

                    print(f'🔄 Reset global count: {global_session_V2.count_global.get()}')
                    modelo_existe_reactivo.set(False)
                    initialized.set(False)
                    return 
        
        
        data_id = input.files_select()  # Captura el ID del archivo seleccionado
        # Actualizar el ID del dataset en la sesión global
        global_session.set_id_dataSet(data_id)
        global_session_V3.modelo_existe.set(False)
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
       
        
        
        data = leer_dataset(
            global_session.get_id_user(),
            global_session.get_id_proyecto(),
            global_session.get_name_proyecto(),
            global_names_reactivos.get_name_file_db(),
            global_session.get_versiones_name(),
            global_session.get_id_version()
        )
        click.set(click() + 1)
        global_session.set_data_set_reactivo(data)
        global_session_V2.count_global.set(1)
        # Validar si el archivo puede cambiar


    
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
        
    delete_button_effects = {}
    @reactive.Effect
    def boton_para_eliminar_name_data_set():
        eliminar_data_set = f"eliminar_version_{global_session.get_id_dataSet()}_{name}"
        if eliminar_data_set not in delete_button_effects:
            @reactive.Effect
            @reactive.event(input[eliminar_data_set])
            def eliminar_version_id():
                base_datos = 'Modeling_App.db'
                tabla = 'name_files'
                columna_objetivo = 'nombre_archivo'
                columna_filtro = 'id_files'
                nombre_version = obtener_valor_por_id(base_datos, tabla, columna_objetivo, columna_filtro, global_session.get_id_dataSet())
                #nombre_version = obtener_valor_por_id(global_session.get_id_dataSet())
                create_modal_v2(f"Seguro que quieres eliminar el Dataset {nombre_version}?", "Confirmar", "Cancelar", "confirmar_id_borrar_dataset", "cancelar_id_dataSet")
        
            delete_button_effects[eliminar_data_set] = eliminar_version_id
            
                
    
    @reactive.Effect
    @reactive.event(input["cancelar_id_dataSet"])
    def remove_modal_Dataset():
        ui.modal_remove()   
     
     
    @reactive.Effect
    @reactive.event(input.confirmar_id_borrar_dataset)
    def remove_versiones_de_parametros():
        if tiene_modelo_generado(global_session.get_id_dataSet()):
            ui.modal_show(create_modal_generic(f"tiene_model", f"Usted tiene un modelo generado para el Dataset: {global_names_reactivos.get_name_file_db()}"))
            return 
        
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
        lista_reactiva.set(lista_de_versiones_new)
        ui.update_select("files_select", choices={str(vers['id_files']): vers['nombre_archivo']
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
    
    
    @reactive.effect
    @reactive.event(input.go_to_principal)
    def _():
        create_navigation_handler("go_to_principal", "Screen_User")
    
     
  
    
    