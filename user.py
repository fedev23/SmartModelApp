from shiny import App, Inputs, Outputs, Session, reactive, ui, render, module
from funciones.nav_panel_User import create_nav_menu_user
from clases.class_user_proyectName import global_user_proyecto
from api import *
from clases.reactives_name import global_names_reactivos
from funciones.help_parametros.valid_columns import replace_spaces_with_underscores
from clases.global_session import global_session
from clases.global_sessionV2 import *
from funciones.funciones_user import create_modal_versiones, show_selected_project_card, create_modal_eliminar_bd, create_modal_v2, button_remove_version
from funciones.utils_2 import *
from logica_users.utils.help_versios import obtener_opciones_versiones, obtener_ultimo_id_version, eliminar_carpeta, mapear_valor_a_clave
from api.db.help_config_db import *
from api.db.up_date import *
from api.db.sqlite_utils import *
from api.db.fun_insert import obtener_ultimo_nombre_file_por_proyecto
from logica_users.help_user_insert.table_user import obtener_o_insertar_usuario
from clases.global_sessionV3 import *
from auth.utils import help_api 
from api.db.sqlite_utils import *
from logica_users.utils.manejo_session import manejo_de_ultimo_seleccionado
from funciones_modelo.global_estados_model import global_session_modelos
from funciones_modelo import help_models 
from api.session_api import consultar_session_api
from funciones.validacionY_Scoring.consultas import comparar_ultimo_file_por_ejecucion

def user_server(input: Inputs, output: Outputs, session: Session, name_suffix):
    user_get = reactive.Value(None)
    proyectos_usuario = reactive.Value(None)
    proceso_eliminar = reactive.Value(False)
    is_initializing = reactive.Value(True)
    id_proyecto_Recien_Creado = reactive.Value(None)
    name_proyecto = reactive.Value(None)
    opciones_param = reactive.Value("")
    opciones_de_versiones_por_proyecto = reactive.Value("")
    ultimo_proyecto_seleccionado =  reactive.Value("")
    ultimo_id_versiones_proyecto = reactive.Value("")
    valor_predeterminado_parms = reactive.Value("")
    boolean_check = reactive.Value(False)
    data_predeterminado = reactive.Value("")
    base_datos = 'Modeling_App.db'
    
    
    def see_session():
        @reactive.effect
        async def enviar_session():
                state = global_session.session_state.get()
                print(state, "valor state>")
                if state["is_logged_in"]:
                    user_id = state["id"]
                    print(user_id, "user id")
                    global_names_reactivos.set_name_file_db("")
                    user_id_hash = user_id.replace("auth0_", "")
                    user_id_hash = obtener_o_insertar_usuario(base_datos, user_id_hash)
                    global_session.has_id_user.set(user_id_hash)
                    global_session.id_user.set(user_id)
                    print("antes de issert!")
                    insertar_usuario_si_no_existe(base_datos, global_session.has_id_user.get())
                    # -> llamo a el valor reactivo para tener la lista de los proyectos por user, dinamicamente, apretar control t y ver la funcion
                    global_session.set_proyectos_usuarios(get_user_projects(user_id))
                    user_get.set(user_id.replace('|', '_'))
                    proyectos_usuario.set(get_user_projects(global_session.get_id_user()))
        
                    #ui.update_select("project_select",choices=proyectos_choise, selected=key_proyecto_mach if key_proyecto_mach else next(iter(proyectos_choise), ""))
        
                    

    see_session()

          

    @reactive.effect
    @reactive.event(input.project_select)  # Escuchar cambios en el selector
    def project_card_container():
        selected_project_id = input.project_select()
        
        manejo_de_ultimo_seleccionado(
            is_initializing=is_initializing,
            input_select_value=input.project_select(),
            ultimo_id_func=lambda: obtener_ultimo_id_seleccionado_proyect(base_datos, "project", "id", global_session.get_id_user()),
            global_set_func=lambda x: global_session.set_id_proyect(x),
            actualizar_ultimo_func=lambda table, column, value: actualizar_ultimo_seleccionado_proyecto(base_datos, table, column, value, global_session.get_id_user() ),
            obtener_ultimo_func=lambda table, column: obtener_ultimo_seleccionado_proyecto(base_datos, table, column, global_session.get_id_user()),
            obtener_opciones_func=lambda: obtener_opciones_versiones(get_user_projects(global_session.get_id_user()), "id", "name"),
            mapear_clave_func=mapear_valor_a_clave,
            ui_update_func=lambda name, choices, selected: ui.update_select(name, choices=choices, selected=selected),
            input_select_name="project_select",
            db_table="project",
            db_column_id="id",
            db_column_name="name"   
        )
        
        
        nombre_proyecto = obtener_nombre_proyecto_por_id(global_session.get_id_proyecto())
        global_session_V3.name_proyecto_original.set(nombre_proyecto)
        
        nombre_proyecto = replace_spaces_with_underscores(nombre_proyecto)
        #global_session_V3.name_proyecto_sin_espacios.set(replace_spaces_with_underscores(nombre_proyecto)) 
        global_session.set_name_proyecto(nombre_proyecto)
        
        proyectos_usuario.set(get_user_projects(global_session.get_id_user()))
        
        
        #EMPIEZA VERSIONES
        versiones_de_proyecto = get_project_versions(global_session.get_id_proyecto())
        opciones_de_versiones_por_proyecto.set(obtener_opciones_versiones(versiones_de_proyecto, "version_id", "nombre_version"))
        
        ultimo_id_versiones_proyecto.set(obtener_ultimo_seleccionado(base_datos, 'version', 'nombre_version'))

        key_versiones_mach = mapear_valor_a_clave(ultimo_id_versiones_proyecto.get(), opciones_de_versiones_por_proyecto.get())
        # Si hay versiones, establece el nombre de la primera versión como predeterminado
        if boolean_check():
            nombre_version = obtener_nombre_version_por_id(global_session.get_id_version())
            global_session_V3.name_version_original.set(nombre_version)
            global_session.set_versiones_name(replace_spaces_with_underscores(nombre_version))
            
        # Actualiza los selectores en la UI
        nombre_version = obtener_nombre_version_por_id(global_session.get_id_version())
        global_session_V3.name_version_original.set(nombre_version)
        global_session.set_versiones_name(replace_spaces_with_underscores(nombre_version))
        
        if (global_session.get_id_user() and
            global_session.get_name_proyecto() and
            global_session.get_id_proyecto() and
            global_session.get_id_version() and
            global_session.get_versiones_name()):   
            api_code = help_api.procesar_starlette_api(global_session.get_id_user(), global_session.get_name_proyecto(), global_session.get_id_proyecto(), global_session.get_id_version(), global_session.get_versiones_name())
        
        ultimo_archivo = obtener_ultimo_nombre_file_por_proyecto(base_datos, 'name_files', global_session.get_id_proyecto())
        global_session_V2.set_dataSet_seleccionado(ultimo_archivo)
        #selected_key = mapear_valor_a_clave(global_session_V2.get_dataSet_seleccionado(), nombre_file.get())
        
        #ui.update_select("project_select",choices=proyectos_choise, selected=key_proyecto_mach if key_proyecto_mach else next(iter(ultimo_proyecto_seleccionado.get()), ""))
        #ui.update_select("files_select_validation_scoring",choices=global_session_V2.get_opciones_name_dataset_Validation_sc(), selected=data_predeterminado.get())
        #ui.update_select("files_select", choices=nombre_file.get(),  selected=selected_key if selected_key else next(iter(nombre_file.get()), ""))
        ui.update_select("other_select", choices=opciones_de_versiones_por_proyecto.get(), selected=key_versiones_mach if key_versiones_mach else next(iter(opciones_de_versiones_por_proyecto.get()), ""))
        #ui.update_select("version_selector", choices=opciones_param.get(), selected=valor_predeterminado_parms.get())
        global_session_V2.count_global.set(0) 
        global_session_V2.boolean_for_change_file.set(False)
        global_session_V2.click_seleccion_niveles_score.set(0)
        
    @output
    @render.ui
    def project_card_container():
            return show_selected_project_card(user_get.get(),  global_session.get_id_proyecto())

    
    
    delete_button_effects = {}  # Diccionario para rastrear los efectos ya definidos
    @reactive.Effect
    def handle_delete_buttons():
        project_id = global_session.get_id_proyecto()
        eliminar_btn_id_proyecto = f"eliminar_proyect_{project_id}"
        
       
        # Verificar si ya existe un manejador para este botón
        if eliminar_btn_id_proyecto not in delete_button_effects:
            @reactive.Effect
            @reactive.event(input[eliminar_btn_id_proyecto])
            def eliminar_proyecto_boton():
                create_modal_eliminar_bd(global_session.get_name_proyecto())

            # Registrar el efecto en el diccionario
            delete_button_effects[eliminar_btn_id_proyecto] = eliminar_proyecto_boton
        
       
    @reactive.Effect
    @reactive.event(input.eliminar_proyecto)
    def eliminar_proyeco_modal():
        eliminar_proyecto(global_session.get_id_proyecto())
        # Actualiza proyectos_usuario después de eliminar el proyecto
        #proyectos_actualizados = get_user_projects(user_get.get())
        proyectos_actualizados = get_records(
            table='project',  # Nombre de la tabla
            columns=['id', 'name'],  # Columnas que deseas recuperar
            where_clause='user_id = ?',  # Cláusula WHERE
            where_params=(user_get.get(),)
        )
        
        
        # Refresca proyectos_usuario con la lista actualizada
        name_proyecto = replace_spaces_with_underscores(global_session.get_name_proyecto())
        path_carpeta_versiones_borrar_salida  = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}'
        path_carpeta_versiones_borrar_entrada  = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_entrada_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}'
        
        eliminar_carpeta(path_carpeta_versiones_borrar_salida)
        eliminar_carpeta(path_carpeta_versiones_borrar_entrada)
        
        proyectos_usuario.set(proyectos_actualizados)
        ultimo_id_versiones_proyecto.set(obtener_ultimo_id_version(proyectos_actualizados, "id"))
        
        
        # Actualiza el selector con los proyectos restantes
        ui.update_select(
            "project_select",
            choices={str(proj['id']): proj['name']
                     for proj in proyectos_actualizados}
        )

        proceso_eliminar.set(True)
        ui.modal_remove()

        # return show_selected_project_card(user_get.get(),  global_session.get_id_proyecto())

   

    @output
    @render.ui
    def create_user_menu():
        return create_nav_menu_user(name_suffix)

    @reactive.effect
    @reactive.event(input[f'version_{name_suffix}'])
    def _():
        # print(id, "estoy en el supuesto id")
        nombre_proyecto = obtener_nombre_proyecto_por_id(
            global_session.get_id_proyecto())
        create_modal_versiones(nombre_proyecto)

    ##BOTON PARA CREAR VERSION ESA ESTA ESTABLECIDO ACA PR UNA COMODIDAD Y CLARIDAD DE VALORES REACTIVOS, LA DEMAS LOICA SE PUEDE ENCONTRAR EN
    #CONFIG SERVER= CONFIGRACION DE VERSIONES
    @reactive.effect
    @reactive.event(input.continuar_version)
    def agregar_ver():
        name = input[f'name_version']()
        id_proyect = global_session.get_id_proyecto()
        global_session.set_id_version(agregar_version(id_proyect, name))
        name = replace_spaces_with_underscores(name)
        
        versiones = get_project_versions(global_session.get_id_proyecto())
        # actualizo la version por proyecto id
        opciones_de_versiones_por_proyecto.set(obtener_opciones_versiones(versiones, "version_id", "nombre_version"))
        ultimo_id_versiones_proyecto.set(obtener_ultimo_id_version(versiones, "version_id"))
        

        ui.update_select("other_select", choices=opciones_de_versiones_por_proyecto.get(), selected=ultimo_id_versiones_proyecto.get())
        global_session.set_proyecto_seleccionado_id(id_proyecto_Recien_Creado.get())
        entrada, salida = crear_carpeta_version_por_proyecto(user_get.get(), global_session.get_id_proyecto(), ultimo_id_versiones_proyecto.get(), name, global_session.get_name_proyecto())
        global_session.set_path_guardar_dataSet_en_proyectos(entrada)
        ui.modal_remove()


    ##EVENTO PARA LA CREACION DEL PROYECTO
    @reactive.effect
    @reactive.event(input[f'start_{name_suffix}'])
    def crear_version():
        global_user_proyecto.create_modal()
        global_user_proyecto.cancelar_buton(input)
        global_user_proyecto.continuar_buton(input)



    @reactive.Effect
    @reactive.event(input.continuar)
    def finalizar_click():
        if global_user_proyecto.click_en_continuar.get() is False:
            # Solo procesa si `click_en_continuar` aún no ha sido activado
            global_user_proyecto.click_en_continuar.set(True)
            ui.modal_remove()

            # Verifica el estado actual antes de proceder
            if global_user_proyecto.click_en_continuar.get():
                user = user_get.get()
                name = input[f'proyecto_nombre']()
                # Crear el proyecto y obtener su ID
                global_session.set_name_proyecto(replace_spaces_with_underscores(name))
                
            
                name_proyecto.set(name)
                global_session.set_id_proyect(add_project(user, name))  # Esta función debería establecer el ID del proyecto recién creado en la sesión global
                proyectos_usuario.set(get_user_projects(user))

                # Aquí asegúrate de que `add_project` o cualquier otro mecanismo te da el `project_id`
                proyect_id = global_session.get_id_proyecto()  # Obtener el ID del proyecto recién creado

                # Establecer el ID en el estado global para que lo puedan usar otros efectos
                id_proyecto_Recien_Creado.set(proyect_id)

                global_session.set_proyecto_seleccionado_id(id_proyecto_Recien_Creado.get())

                 
                # Actualiza el selector con los proyectos restantes
                proyectos = get_user_projects(user_get.get())
                opciones = {str(proj['id']): proj['name'] for proj in proyectos}
                ultimo_proyecto_id = str(proyectos[-1]['id'])
                
                ui.update_select(
                    "project_select",
                    choices=opciones,
                    selected=ultimo_proyecto_id  # Preselecciona el último ID
                )
                global_session.set_id_user(user_get())
                name = replace_spaces_with_underscores(name)
                crear_carpeta_proyecto(user_get.get(), global_session.get_id_proyecto(), name)
                data_Set = get_datasets_directory(user_get.get(), global_session.get_id_proyecto(), global_session.get_name_proyecto())
                #global_session.set_path_guardar_dataSet_en_proyectos(data_Set)
                global_names_reactivos.set_name_file_db("")
                #global_names_reactivos.get_name_file_db()
                # Reinicia el estado de click en continuar
                global_user_proyecto.click_en_continuar.set(False)

    
    
    
    


    def setup_modal_cancels(cancel_inputs):
        cancels = {}
        for input_name, input_trigger in cancel_inputs.items():
            @reactive.effect
            @reactive.event(input_trigger)
            def cancel_handler():
                return ui.modal_remove()
            cancels[input_name] = cancel_handler
        return cancels

# Aquí defines qué inputs quieres asociar a qué nombres
    cancel_handlers = setup_modal_cancels({
        'version': input.cancelar_eliminar,  
        'cancel_user': input.cancelar,
        'cancelar_version': input.cancelar_version,
        'cancel_overwrite_Desarrollo': input.cancel_overwrite_Desarrollo
    })
    

    