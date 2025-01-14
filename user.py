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
from api.db.sqlite_utils import *
from auth.utils import help_api 
from api.db.sqlite_utils import *
from logica_users.utils.manejo_session import manejo_de_ultimo_seleccionado
from funciones_modelo.global_estados_model import global_session_modelos
from funciones_modelo import help_models 

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
        def enviar_session():
            if global_session.proceso.get():
                state = global_session.session_state.get()
                if state["is_logged_in"]:
                    user_id = state["id"]
                    global_session.id_user.set(user_id)
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
            ultimo_id_func=lambda: obtener_ultimo_id_seleccionado(base_datos, "project", "id"),
            global_set_func=lambda x: global_session.set_id_proyect(x),
            actualizar_ultimo_func=lambda table, column, value: actualizar_ultimo_seleccionado(base_datos, table, column, value),
            obtener_ultimo_func=lambda table, column: obtener_ultimo_seleccionado(base_datos, table, column),
            obtener_opciones_func=lambda: obtener_opciones_versiones(get_user_projects(global_session.get_id_user()), "id", "name"),
            mapear_clave_func=mapear_valor_a_clave,
            ui_update_func=lambda name, choices, selected: ui.update_select(name, choices=choices, selected=selected),
            input_select_name="project_select",
            db_table="project",
            db_column_id="id",
            db_column_name="name"
        )

        
    
        nombre_proyecto = obtener_nombre_proyecto_por_id(global_session.get_id_proyecto())
        global_session.set_name_proyecto(nombre_proyecto)
        
        proyectos_usuario.set(get_user_projects(global_session.get_id_user()))
        
        proyectos_choise = obtener_opciones_versiones(proyectos_usuario.get(), "id", "name")
        ultimo_proyecto_seleccionado.set(obtener_ultimo_seleccionado(base_datos, 'project', 'name'))
        key_proyecto_mach = mapear_valor_a_clave(ultimo_proyecto_seleccionado.get(), proyectos_choise)

        #EMPIEZA VERSIONES
        versiones_de_proyecto = get_project_versions(global_session.get_id_proyecto())
        opciones_de_versiones_por_proyecto.set(obtener_opciones_versiones(versiones_de_proyecto, "version_id", "nombre_version"))
        
        ultimo_id_versiones_proyecto.set(obtener_ultimo_seleccionado(base_datos, 'version', 'nombre_version'))

        key_versiones_mach = mapear_valor_a_clave(ultimo_id_versiones_proyecto.get(), opciones_de_versiones_por_proyecto.get())
        # Si hay versiones, establece el nombre de la primera versión como predeterminado
        if boolean_check():
            nombre_version = obtener_nombre_version_por_id(global_session.get_id_version())
            global_session.set_versiones_name(nombre_version)
            
        # Obtiene y configura las versiones de parámetros
        versiones_parametros  = get_project_versions_param_mejorada(global_session.get_id_proyecto(), global_session.get_id_version())
            # 
        opciones_param.set(obtener_opciones_versiones(versiones_parametros, "id_jsons", "nombre_version"))
        valor_predeterminado_parms.set(obtener_ultimo_id_version(versiones_parametros, "id_jsons"))
        ##Actualizo tambien los dataSet de Validacion y scroing
        nombre_files_validacion_sc = get_records(
            table='validation_scoring',
            columns=['id_validacion_sc', 
                    'nombre_archivo_validation_sc', 
                    'fecha_de_carga'],
            where_clause='project_id = ?',  # Cambiado para usar project_id directamente
            where_params=(global_session.get_id_proyecto(),)
        )
    
        
        global_session_V2.set_opciones_name_dataset_Validation_sc(obtener_opciones_versiones(nombre_files_validacion_sc, "id_validacion_sc", "nombre_archivo_validation_sc"))
        data_predeterminado.set(obtener_ultimo_id_version(nombre_files_validacion_sc, 'id_validacion_sc'))

        #LEEO ELDATA SET SI EXISTE
        # Actualiza los selectores en la UI
        nombre_version = obtener_nombre_version_por_id(global_session.get_id_version())
        global_session.set_versiones_name(nombre_version)

        if (global_session.get_id_user() and
            global_session.get_name_proyecto() and
            global_session.get_id_proyecto() and
            global_session.get_id_version() and
            global_session.get_versiones_name()):   
            api_code = help_api.procesar_starlette_api(global_session.get_id_user(), global_session.get_name_proyecto(), global_session.get_id_proyecto(), global_session.get_id_version(), global_session.get_versiones_name())
        
        ultimo_archivo = obtener_ultimo_seleccionado(base_datos, 'name_files', 'nombre_archivo')
        global_session_V2.set_dataSet_seleccionado(ultimo_archivo)
        #selected_key = mapear_valor_a_clave(global_session_V2.get_dataSet_seleccionado(), nombre_file.get())
        
        ui.update_select("project_select",choices=proyectos_choise, selected=key_proyecto_mach if key_proyecto_mach else next(iter(ultimo_proyecto_seleccionado.get()), ""))
        ui.update_select("files_select_validation_scoring",choices=global_session_V2.get_opciones_name_dataset_Validation_sc(), selected=data_predeterminado.get())
        #ui.update_select("files_select", choices=nombre_file.get(),  selected=selected_key if selected_key else next(iter(nombre_file.get()), ""))
        ui.update_select("other_select", choices=opciones_de_versiones_por_proyecto.get(), selected=key_versiones_mach if key_versiones_mach else next(iter(opciones_de_versiones_por_proyecto.get()), ""))
        ui.update_select("version_selector", choices=opciones_param.get(), selected=valor_predeterminado_parms.get())
        global_session_V2.count_global.set(0) 
        global_session_V2.boolean_for_change_file.set(False)
        
    @output
    @render.ui
    def project_card_container():
            return show_selected_project_card(user_get.get(),  global_session.get_id_proyecto())

    
    @reactive.Effect
    @reactive.event(input["cancelar"])
    def cancelar_eliminacion_version():
        return ui.modal_remove()
    
    @reactive.Effect
    @reactive.event(input["cancelar_version"])
    def cancelar_eliminacion_version():
        return ui.modal_remove()
    
    delete_button_effects = {}  # Diccionario para rastrear los efectos ya definidos
    @reactive.Effect
    def handle_delete_buttons():
        project_id = global_session.get_id_proyecto()
        eliminar_btn_id_proyecto = f"eliminar_proyect_{project_id}"
        
        print("eliminar_btn_id:", eliminar_btn_id_proyecto)

        # Verificar si ya existe un manejador para este botón
        if eliminar_btn_id_proyecto not in delete_button_effects:
            print("Creando efecto para:", eliminar_btn_id_proyecto)

            @reactive.Effect
            @reactive.event(input[eliminar_btn_id_proyecto])
            def eliminar_proyecto_boton():
                create_modal_eliminar_bd(global_session.get_name_proyecto())

            # Registrar el efecto en el diccionario
            delete_button_effects[eliminar_btn_id_proyecto] = eliminar_proyecto_boton
        else:
            print("Efecto ya definido para:", eliminar_btn_id_proyecto)    
   
       
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
        path_carpeta_versiones_borrar_salida  = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{name_proyecto}'
        path_carpeta_versiones_borrar_entrada  = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_entrada_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{name_proyecto}'
        
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

    @reactive.Effect
    @reactive.event(input["cancelar_eliminar"])
    def canacelar_eliminacion():
       return ui.modal_remove()


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

    @reactive.effect
    @reactive.event(input.cancelar_eliminar)
    def cancel_version():
        return ui.modal_remove()
        # agregar_version


    ##BOTON PARA CREAR VERSION ESA ESTA ESTABLECIDO ACA PR UNA COMODIDAD Y CLARIDAD DE VALORES REACTIVOS, LA DEMAS LOICA SE PUEDE ENCONTRAR EN
    #CONFIG SERVER= CONFIGRACION DE VERSIONES
    @reactive.effect
    @reactive.event(input.continuar_version)
    def agregar_ver():
        name = input[f'name_version']()
        id_proyect = global_session.get_id_proyecto()
        global_session.set_id_version(agregar_version(id_proyect, name))

        
        versiones = get_project_versions(global_session.get_id_proyecto())
        # actualizo la version por proyecto id
        opciones_de_versiones_por_proyecto.set(obtener_opciones_versiones(versiones, "version_id", "nombre_version"))
        ultimo_id_versiones_proyecto.set(obtener_ultimo_id_version(versiones, "version_id"))
        

        ui.update_select("other_select", choices=opciones_de_versiones_por_proyecto.get(), selected=ultimo_id_versiones_proyecto.get())
        global_session.set_proyecto_seleccionado_id(id_proyecto_Recien_Creado.get())
        name_2 = replace_spaces_with_underscores(name)
        entrada, salida = crear_carpeta_version_por_proyecto(user_get.get(), global_session.get_id_proyecto(), ultimo_id_versiones_proyecto.get(), name_2, global_session.get_name_proyecto())
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
                global_session.set_name_proyecto(name)
            
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

                # Reinicia el estado de click en continuar
                global_user_proyecto.click_en_continuar.set(False)

    
    
    
    @reactive.effect
    def recargar_values_of_config():
        if global_estados.value_boolean_for_values_in_config.get():
            config = obtener_configuracion_por_hash(base_datos, global_session.get_id_user())
            print(config, "que pasa con config?")
            valor_min_seg, valor_max_seg, num_select_filas, value_dark_or_light = config.values()
            print(valor_min_seg, "que tiene valor min??")
            ui.update_numeric(
                "min_value",
                #label="Ingrese el valor minimo para la configuracion de segmentacion",
                value=valor_min_seg,
                #min=3,
                #max=10,
            ) 

    @reactive.effect
    @reactive.event(input.close)
    async def _():
        await session.close()
