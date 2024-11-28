from shiny import App, Inputs, Outputs, Session, reactive, ui, render, module
from funciones.nav_panel_User import create_nav_menu_user
from clases.class_user_proyectName import global_user_proyecto
from api import *
from clases.global_session import global_session
from clases.global_reactives import global_estados
from clases.global_sessionV2 import *
from funciones.funciones_user import create_modal_versiones, show_selected_project_card, create_modal_eliminar_bd, create_modal_v2, button_remove_version
from funciones.utils_2 import crear_carpeta_proyecto, crear_carpeta_version_por_proyecto, get_datasets_directory
from funciones.help_versios import obtener_opciones_versiones, obtener_ultimo_id_version


def user_server(input: Inputs, output: Outputs, session: Session, name_suffix):
    user_get = reactive.Value(None)
    proyect_ok = reactive.Value(False)
    proyectos_usuario = reactive.Value(None)
    proceso_eliminar = reactive.Value(False)
    version_options = reactive.Value({})
    versiones_por_proyecto = reactive.Value(None)
    nombre_file = reactive.Value(None)
    id_proyecto_Recien_Creado = reactive.Value(None)
    name_proyecto = reactive.Value(None)
    opciones_param = reactive.Value("")
    valor_predeterminado_parms = reactive.Value("")
    boolean_check = reactive.Value(False)
    data_predeterminado = reactive.Value("")
    

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

    see_session()

    @reactive.effect
    def capturar_num_seleccionador_dataSet():
        select_number_data_set = input.number_choice()
        global_estados.set_numero_dataset(select_number_data_set)

    @reactive.effect
    @reactive.event(input.project_select)  # Escuchar cambios en el selector
    def project_card_container():
        # Captura el ID del proyecto seleccionado
        selected_project_id = input.project_select()
        #print(selected_project_id, "proyecto")
        global_session.set_id_proyect(selected_project_id)

        nombre_proyecto = obtener_nombre_proyecto_por_id(global_session.get_id_proyecto())
        global_session.set_name_proyecto(nombre_proyecto)

        # Obtiene las versiones del proyecto
        versiones = get_project_versions(global_session.get_id_proyecto())

        # Configura boolean_check según la presencia de versiones
        if versiones:
            boolean_check.set(True)
            version_options.set({
                str(version['version_id']): version['nombre_version']
                for version in versiones
            })
        else:
            boolean_check.set(False)
            version_options.set({"": "No hay versiones"})
        
        # Si hay versiones, establece el nombre de la primera versión como predeterminado
        if boolean_check():
            nombre_version = obtener_nombre_version_por_id(global_session.get_id_version())
            global_session.set_versiones_name(nombre_version)
            

        # Obtiene los archivos relacionados con el proyecto
        files_name = get_records(table='name_files',
            columns=['id_files', 'nombre_archivo', 'fecha_de_carga'],
            where_clause='project_id = ?',
            where_params=(global_session.get_id_proyecto(),))
        
        nombre_file.set({
            str(file['id_files']): file['nombre_archivo']
            for file in files_name
        } if files_name else {"": "No hay archivos"})

        # Obtiene y configura las versiones de parámetros
        versiones_parametros = get_project_versions_param(global_session.get_id_proyecto())
        opciones_param.set(obtener_opciones_versiones(versiones_parametros, "id_jsons", "nombre_version"))
        valor_predeterminado_parms.set(obtener_ultimo_id_version(versiones_parametros, "id_jsons"))

        # Crea el path para guardar datasets
        data_Set = crear_carpeta_proyecto(
            user_get.get(), global_session.get_id_proyecto(), global_session.get_name_proyecto()
        )
        global_session.set_path_guardar_dataSet_en_proyectos(data_Set)
        
        
        ##Actualizo tambien los dataSet de Validacion y scroing
        nombre_files_validacion_sc = get_records(
                table='validation_scoring',
                columns=['id_validacion_sc', 'nombre_archivo_validation_sc', 'fecha_de_carga'],
                where_clause='project_id = ?',
                where_params=(global_session.get_id_proyecto(),)
            )
        
        global_session_V2.set_opciones_name_dataset_Validation_sc(obtener_opciones_versiones(nombre_files_validacion_sc, "id_validacion_sc", "nombre_archivo_validation_sc"))
        data_predeterminado.set(obtener_ultimo_id_version(nombre_files_validacion_sc, "id_validacion_sc"))
        
        
        
        # Actualiza los selectores en la UI
        ui.update_select("files_select_validation_scoring",choices=global_session_V2.get_opciones_name_dataset_Validation_sc(), selected=data_predeterminado.get())
        ui.update_select("files_select", choices=nombre_file.get())
        ui.update_select("other_select", choices=version_options.get())
        ui.update_select("version_selector", choices=opciones_param.get(), selected=valor_predeterminado_parms.get())

    @output
    @render.ui
    def project_card_container():
        if proyect_ok:
            return show_selected_project_card(user_get.get(),  global_session.get_id_proyecto())

    @reactive.effect
    @reactive.event(input.other_select)  # Escuchar cambios en el selector
    def project_card_container():
        versiones_id = input.other_select()  # Captura el ID seleccionado
        global_session.set_id_version(versiones_id)
        nombre_version = obtener_nombre_version_por_id(global_session.get_id_version())
        global_session.set_versiones_name(nombre_version)
        

    @output
    @render.ui
    def button_remove_versions():
        if proyect_ok:
            return button_remove_version(global_session.get_id_proyecto(), global_session.get_id_version())

    # boton para eliminar proyecto

    @reactive.Effect
    def boton_para_eliminar_version():
        eliminar_version_id = f"eliminar_version_{global_session.get_id_version()}"
        @reactive.Effect
        @reactive.event(input[eliminar_version_id])
        def eliminar_version_id():
            nombre_version = obtener_nombre_version_por_id(global_session.get_id_version())
            create_modal_v2(f"Seguro que quieres eliminar la version {nombre_version}?", "Confirmar", "Cancelar", "confirmar_id", "cancelar_id")
            

    @reactive.Effect
    @reactive.event(input["confirmar_id"])
    def eliminar_version_proyecto():
        eliminar_version("version", "version_id", global_session.get_id_version())
        columnas = ['version_id', 'nombre_version', 'execution_date']
        lista_de_versiones_new = obtener_versiones_por_proyecto(global_session.get_id_proyecto(), columnas, "version", "project_id")

        versiones_por_proyecto.set(lista_de_versiones_new)
        ui.update_select(
            "other_select",
            choices={str(vers['version_id']): vers['nombre_version']
                     for vers in lista_de_versiones_new}
        )
        ui.modal_remove()

    @reactive.Effect
    @reactive.event(input["confirmar_id_dataset"])
    def eliminar_dataset():
        eliminar_version('name_files', 'id_files',global_session.get_id_dataSet())
        columnas = ['id_files', 'nombre_archivo', 'fecha_de_carga']
        lista_de_versiones_new = obtener_versiones_por_proyecto(
            global_session.get_id_proyecto(), columnas, "name_files", "project_id")
        nombre_file.set(lista_de_versiones_new)
        ui.update_select(
            "files_select",
            choices={str(vers['id_files']): vers['nombre_archivo']
                     for vers in lista_de_versiones_new}
        )
        ui.modal_remove()

    # boton para eliminar proyecto

    @reactive.Effect
    def handle_delete_buttons():
        project_id = global_session.get_id_proyecto()
        eliminar_btn_id = f"eliminar_proyect_{project_id}"

        @reactive.Effect
        @reactive.event(input[eliminar_btn_id])
        def eliminar_proyecto_boton():
            create_modal_eliminar_bd()

    @reactive.Effect
    @reactive.event(input["eliminar_proyecto_modal"])
    def eliminar_proyeco_modal():
        session_id = global_session.get_id_proyecto()
        
        eliminar_proyecto(global_session.get_id_proyecto())
        # Actualiza proyectos_usuario después de eliminar el proyecto
        proyectos_actualizados = get_user_projects(user_get.get())
        # Refresca proyectos_usuario con la lista actualizada
        proyectos_usuario.set(proyectos_actualizados)

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
        ui.modal_remove()

    @output
    @render.ui
    def nombre_proyecto_user():
        return ui.div()

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
        ui.modal_remove()
        # agregar_version


    @reactive.effect
    @reactive.event(input.continuar_version)
    def agregar_ver():
        name = input[f'name_version']()
        id_proyect = global_session.get_id_proyecto()
        agregar_version(id_proyect, name)
      
        versiones = get_project_versions(global_session.get_id_proyecto())
        # actualizo la version por proyecto id
        version_options.set({str(version['version_id']): version['nombre_version']
                            for version in versiones}if versiones else {"": "No hay versiones"})
        ui.update_select("other_select", choices=version_options.get())
        global_session.set_proyecto_seleccionado_id(id_proyecto_Recien_Creado.get())
       
        crear_carpeta_version_por_proyecto(user_get.get(), global_session.get_id_proyecto(), global_session.get_id_version(), name, global_session.get_name_proyecto())
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
                ui.update_select("project_select", choices={str(proj['id']): proj['name'] for proj in get_user_projects(user_get.get())}
                )

                global_session.set_id_user(user_get())
                crear_carpeta_proyecto(user_get.get(), global_session.get_id_proyecto(), name)
                data_Set = get_datasets_directory(user_get.get(), global_session.get_id_proyecto(), global_session.get_name_proyecto())
                global_session.set_path_guardar_dataSet_en_proyectos(data_Set)

                # Reinicia el estado de click en continuar
                global_user_proyecto.click_en_continuar.set(False)

    
            
    @reactive.effect
    @reactive.event(input[f'settings_{name_suffix}'])
    async def log_out():
        create_navigation_handler('settings_user', 'Screen_Login')
        await session.close()

    @reactive.effect
    @reactive.event(input.close)
    async def _():
        await session.close()

    def create_navigation_handler(input_id, screen_name):
        @reactive.Effect
        @reactive.event(input[input_id])
        async def navigate():
            await session.send_custom_message('navigate', screen_name)

