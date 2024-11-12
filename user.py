from shiny import App, Inputs, Outputs, Session, reactive, ui, render, module
from funciones.nav_panel_User import create_nav_menu_user
from clases.class_user_proyectName import global_user_proyecto
from api import *
from clases.global_session import global_session
from clases.global_reactives import global_estados
from funciones.funciones_user import create_modal_versiones, show_selected_project_card, create_modal_eliminar_bd, create_modal_v2, button_remove_version
from funciones.utils_2 import crear_carpeta_proyecto, crear_carpeta_version_por_proyecto


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
        # Captura el ID del proyecto seleccionado
        selected_project_id = input.project_select()
        global_session.set_id_proyect(selected_project_id)

        # Obtén el nombre del proyecto por el ID
        nombre_proyecto = obtener_nombre_proyecto_por_id(
            global_session.get_id_proyecto())
        global_session.proyecto_seleccionado.set(nombre_proyecto)

        # Obtiene las versiones del proyecto
        versiones = get_project_versions(global_session.get_id_proyecto())
        version_options.set(
            {str(version['version_id']): version['nombre_version']
             for version in versiones}
            if versiones else {"": "No hay versiones"}
        )

        # Obtiene los archivos relacionados con el proyecto
        files_name = get_records(global_session.get_id_proyecto())

        nombre_file.set({str(file['id_files']): file['nombre_archivo']
                        for file in files_name}if files_name else {"": "No hay archivos"})
        # print(nombre_file.get(), "estoy en el get")

        ui.update_select("files_select", choices=nombre_file.get())
        ui.update_select("other_select", choices=version_options.get())
        # ui.update_select("select_file", choices=nombre_file.get())

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
            nombre_version = obtener_nombre_version_por_id(
                global_session.get_id_version())
            create_modal_v2(
                f"Seguro que quieres eliminar la version {nombre_version}?", "Confirmar", "Cancelar", "confirmar_id", "cancelar_id")

    @reactive.Effect
    @reactive.event(input["confirmar_id"])
    def eliminar_version_proyecto():
        eliminar_version("version", "version_id",
                         global_session.get_id_version())
        columnas = ['version_id', 'nombre_version', 'execution_date']
        lista_de_versiones_new = obtener_versiones_por_proyecto(global_session.get_id_proyecto(), columnas, "version", "project_id")

        # lista_de_versiones_new = obtener_versiones_por_proyecto(global_session.get_id_proyecto())
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
        eliminar_version('name_files', 'id_files',
                         global_session.get_id_dataSet())
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
        print(session_id,"tenog session id")
        eliminar_proyecto(global_session.get_id_proyecto())
        print(global_session.get_id_proyecto())
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
        print(f"imprimo id, {id_proyect}")
        agregar_version(id_proyect, name)
        versiones = get_project_versions(global_session.get_id_proyecto())
        # actualizo la version por proyecto id
        version_options.set({str(version['version_id']): version['nombre_version']
                            for version in versiones}if versiones else {"": "No hay versiones"})
        print(version_options.get())
        ui.update_select("other_select", choices=version_options.get())
        print(id_proyecto_Recien_Creado.get(), "estoy en la session")
        crear_carpeta_version_por_proyecto(user_get.get(),id_proyecto_Recien_Creado.get(), global_session.get_id_version(), name, name_proyecto.get())
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
                # init_bd.list_tables()
                name_proyecto.set(name)
                add_project(user, name)
                proyectos_usuario.set(get_user_projects(user))
                proyect_id= global_session.get_id_proyecto()
                ##CRE ESTE NUEVOEFECTO REACTIVO TEMPORAL, YA QUE NOSE POR QUE CAMBIA DE VALOR EL GLOBALSESSION ID
                id_proyecto_Recien_Creado.set(proyect_id)
                print(global_session.get_id_proyecto(), "este es el id del proyecto")
                crear_carpeta_proyecto(user_get.get(), global_session.get_id_proyecto(), name)
            
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
                        # Alineado debajo del selector
                        ui.output_ui("project_card_container"),
                    ),
                    # Segunda columna para el selector de versiones y el botón de eliminar versiones
                    ui.column(
                        6,  # Ancho de la columna
                        ui.input_select(
                            "other_select",
                            "Versiones",
                            {'a': "a"},
                            width="100%"
                        ),
                        # Alineado debajo del selector
                        ui.output_ui("button_remove_versions"),
                    ),
                ),
                ui.div(class_="mt-5"),  # Espaciado entre las filas

                # Fila para el input de archivo y la tarjeta
                ui.row(
                    ui.column(
                        12,  # Ancho de la columna para la tarjeta completa
                        ui.card(
                            ui.row(
                                # Primera columna para el input de archivo
                                ui.column(
                                    6,  # Ocupa el 50% del espacio de la tarjeta
                                    ui.input_file(
                                        "file_desarollo",
                                        "",
                                        button_label='Seleccionar archivo',
                                        placeholder='Subir un archivo',
                                        accept=[".csv", ".txt"],
                                        width="60%"  # Aseguramos que el input ocupe todo el ancho de la columna
                                    )
                                ),
                                # Segunda columna para el input de select
                                ui.column(
                                    6,  # Ocupa el 50% del espacio de la tarjeta
                                    ui.input_select(
                                        "files_select",
                                        "DataSets",
                                        {'a': "a"},
                                        width="60%"  # Aseguramos que el select ocupe todo el ancho de la columna
                                    ),
                                    ui.output_ui("remove_dataset"),
                                )
                            ),
                            style="height: 150px;"  # Ajusta la altura de la tarjeta según sea necesario
                        )
                    )
                )
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

