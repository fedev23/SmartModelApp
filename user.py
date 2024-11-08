from shiny import App, Inputs, Outputs, Session, reactive, ui, render, module
from funciones.nav_panel_User import create_nav_menu_user
from clases.class_user_proyectName import global_user_proyecto
from api import *
from clases.global_session import global_session
from clases.global_reactives import global_estados
from funciones.funciones_user import create_modal_versiones, show_selected_project_card, create_modal_eliminar_bd, create_modal_v2, button_remove_version


def user_server(input: Inputs, output: Outputs, session: Session, name_suffix):
    user_get = reactive.Value(None)
    proyect_ok = reactive.Value(False)
    proyectos_usuario = reactive.Value(None)
    proceso_eliminar = reactive.Value(False)
    version_options = reactive.Value ({})
    versiones_por_proyecto = reactive.Value(None)
    

    def see_session():
        @reactive.effect
        def enviar_session():
            if global_session.proceso.get():
                state = global_session.session_state.get()
                if state["is_logged_in"]:
                    user_id = state["id"]
                    global_session.id_user.set(user_id)
                    # -> llamo a el valor reactivo para tener la lista de los proyectos por user, dinamicamente, apretar control t y ver la funcion
                    proyectos_usuario.set(get_user_projects(user_id))
                    user_get.set(user_id.replace('|', '_'))

    see_session()

    @reactive.effect
    def capturar_num_seleccionador_dataSet():
        select_number_data_set = input.number_choice()
        global_estados.set_numero_dataset(select_number_data_set)

    @reactive.effect
    @reactive.event(input.project_select)  # Escuchar cambios en el selector
    def project_card_container():
        selected_project_id = input.project_select()  # Captura el ID seleccionado
        global_session.set_id_proyect(selected_project_id)
        nombre_proyecto = obtener_nombre_proyecto_por_id(global_session.get_id_proyecto())
        global_session.proyecto_seleccionado.set(nombre_proyecto)
        versiones = get_project_versions(global_session.get_id_proyecto())
        version_options.set({str(version['version_id']): version['nombre_version'] for version in versiones}if versiones else {"": "No hay versiones"})
        #print(version_options.get())
        ui.update_select("other_select", choices=version_options.get())
        
        
        
    @output
    @render.ui
    def project_card_container():
        if proyect_ok:
            return show_selected_project_card(user_get.get(),  global_session.get_id_proyecto())
        
    
    @reactive.effect
    @reactive.event(input.other_select)  # Escuchar cambios en el selector
    def project_card_container():
        versiones_id = input.other_select()  # Captura el ID seleccionado
        print(versiones_id)
        global_session.set_id_version(versiones_id)
        print(global_session.get_id_version())
        print(versiones_id, "id versiones")
    
        
        
    @output
    @render.ui
    def button_remove_versions():
            return button_remove_version(global_session.get_id_proyecto(), global_session.get_id_version())
        
    
    # boton para eliminar proyecto
    @reactive.Effect
    def boton_para_eliminar_version():
        eliminar_version_id = f"eliminar_version_{global_session.get_id_version()}"

        @reactive.Effect
        @reactive.event(input[eliminar_version_id])
        def eliminar_version_id():
            nombre_version = obtener_nombre_version_por_id(global_session.get_id_version())
            print(nombre_version)
            create_modal_v2(f"Seguro que quieres eliminar la version {nombre_version}?", "Confirmar", "Cancelar", "confirmar_id", "cancelar_id")

    
    @reactive.Effect
    @reactive.event(input["confirmar_id"])
    def eliminar_version_proyecto():
        print("pase")
        
        eliminar_version(global_session.get_id_version())
        lista_de_versiones_new = obtener_versiones_por_proyecto(global_session.get_id_proyecto())
        versiones_por_proyecto.set(lista_de_versiones_new)
        ui.update_select(
                "other_select",
                choices={str(vers['version_id']): vers['nombre_version']
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
        # global_user_proyecto.click_en_continuar.set(True)

    @reactive.effect
    @reactive.event(input.cancelar_eliminar)
    def cancel_version():
        ui.modal_remove()
        # agregar_version

    @reactive.effect
    @reactive.event(input.continuar_version)
    def agregar_ver():
        name = input[f'name_version']()
        print(name)
        id_proyect = global_session.get_id_proyecto()
        print(f"imprimo id, {id_proyect}")
        agregar_version(id_proyect, name)
        versiones = get_project_versions(global_session.get_id_proyecto())
        ##actualizo la version por proyecto id
        version_options.set({str(version['version_id']): version['nombre_version'] for version in versiones}if versiones else {"": "No hay versiones"})
        print(version_options.get())
        ui.update_select("other_select", choices=version_options.get())
        ui.modal_remove()

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
                # init_bd.list_tables()
                add_project(user, name)
                proyectos_usuario.set(get_user_projects(user))
                print(proyectos_usuario.get())
                create_navigation_handler('continuar', 'Screen_Desarollo')
                global_user_proyecto.click_en_continuar.set(False)

    @output
    @render.ui
    def devolver_acordeon():
        projects = proyectos_usuario.get()  # Obtiene la lista actual de proyectos

        if projects:
            project_options = {
                str(project['id']): project['name'] for project in projects
            }
            return ui.div(
                ui.row(
                    # Primera columna para el selector de proyectos y el botón
                    ui.column(
                        6,  # Ancho de la columna
                        ui.input_select(
                            "project_select",
                            "Selecciona un proyecto:",
                            project_options,
                            width="60%"
                        ),
                         ui.output_ui("project_card_container"),# Alineado debajo del selector
                    ),
                    # Segunda columna para el selector de versiones y la tarjeta
                    ui.column(
                        6,  # Ancho de la columna
                        ui.input_select(
                            "other_select",
                            "Versiones",
                            {'a': "a"},
                            width="60%"
                        ),
                          ui.output_ui("button_remove_versions"),   # Alineado debajo del selector
                    )
                ),
                ui.div(class_="mt-2"),
                ui.div(
                    ui.input_file(
                        "file_desarollo",
                        "Cargar archivo de datos:",
                        button_label='Seleccionar archivo',
                        placeholder='Selecciona un archivo',
                        accept=[".csv", ".txt"],
                        width="30%"
                    ),
                ),
            )
            
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

    # create_navigation_handler('finalizar', 'Screen_Desarollo')

    create_navigation_handler('load_Validacion_user', 'Screen_valid')
    create_navigation_handler('load_Validacion_user', 'Screen_valid')
    create_navigation_handler('screen_Desarollo_user', 'Screen_Desarollo')
    create_navigation_handler('screen_Produccion_user', 'Screen_Porduccion')
    create_navigation_handler('ir_result_user', 'Screen_Resultados')
    create_navigation_handler('ir_carga_user', 'Screen_Desarollo')
    create_navigation_handler('ir_modelos_user', 'Screen_3')
    create_navigation_handler('screen_in_sample_user', 'screen_in_sample')

    @reactive.Effect
    @reactive.event(input.ir_carga_archivos)
    async def go_to_carga_load_fila():
        await session.send_custom_message('navigate', 'Screen_Desarollo')
