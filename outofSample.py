from shiny import reactive, render, ui
from funciones.create_param import create_screen
from funciones.create_nav_menu import create_nav_menu
from clases.class_screens import ScreenClass
from clases.class_user_proyectName import global_user_proyecto
from global_var import global_data_loader_manager
from funciones.utils_2 import errores, validar_proyecto


def server_out_of_sample(input, output, session, name_suffix):
    # Obtener el loader de datos desde el manage
    proceso_a_completado = reactive.Value(False)
    directorio_validacion = r'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat'
    hay_error = reactive.Value(False)
    mensaje = reactive.Value("")
    name = "Out-Of-Sample"
    data_loader = global_data_loader_manager.get_loader(name_suffix)

    # Instanciamos la clase ScreenClass
    screen_instance = ScreenClass(directorio_validacion, name_suffix)

    @output
    @render.text
    def nombre_proyecto_validacion():
        return f'Proyecto: {global_user_proyecto.mostrar_nombre_proyecto_como_titulo()}'

    @output
    @render.ui
    def nav_out_to_sample():
        return create_nav_menu(name_suffix, name)

    @reactive.Effect
    @reactive.event(input.file_validation)
    async def loadOutSample():
        print("entre")
        await screen_instance.load_data(input.file_validation, input.delimiter_validacion_out_to, name_suffix)

    @reactive.Effect
    @reactive.event(input[f'load_param_{name_suffix}'])
    def desarollo_out_to_and_valid():
        # 1. Validar si el dataset está cargado
        df = data_loader.getDataset()
        if df is None:
            mensaje.set(f"No se seleccionó ningún archivo en {name}")
            return  # Detener la ejecución si no hay dataset

        # 2. Validar si el proyecto está asignado
        proyecto_nombre = global_user_proyecto.get_nombre_proyecto()
        if not validar_proyecto(proyecto_nombre):
            mensaje.set(f"Es necesario tener un proyecto asignado o creado para continuar en {name}")
            return  # Detener la ejecución si no hay proyecto asignado

        # 3. Continuar si ambas validaciones anteriores pasan
        if screen_instance.proceso_a_completado.get():
            create_navigation_handler(f'load_param_{name_suffix}', 'Screen_3')
            ui.update_accordion("my_accordion", show=["out_to_sample"])


    @output
    @render.text
    def error_in_validacion():
        return errores(mensaje)

    @output
    @render.data_frame
    def summary_data_validacion_out_to_sample():
        return screen_instance.render_data_summary()

    @output
    @render.ui
    def mostrarOut():
        if proceso_a_completado.get():
            print("entre")
            return ui.input_action_button("ir_ejecucion_validacion_out_to", "Ir a ejecución")
        return ui.TagList()

    # retorno funcion de parametros
    @output
    @render.ui
    def screen_content():
        return create_screen(name_suffix)

    def create_navigation_handler(input_id, screen_name):
        @reactive.Effect
        @reactive.event(input[input_id])
        async def navigate():
            await session.send_custom_message('navigate', screen_name)

    create_navigation_handler('start_validacion_', 'Screen_User')
    create_navigation_handler(
        'screen_in_sample_validacion', 'screen_in_sample')
    create_navigation_handler(
        'screen_Desarollo_validacion', 'Screen_Desarollo')
    create_navigation_handler(
        'load_Validacion_out_to_validacion', 'Screen_valid')
    create_navigation_handler(
        'screen_Produccion_validacion', 'Screen_Porduccion')
    create_navigation_handler('ir_modelos_validacion', 'Screen_3')
    create_navigation_handler("ir_result_validacion", "Screen_Resultados")
    create_navigation_handler("volver_validacion", "Screen_User")
