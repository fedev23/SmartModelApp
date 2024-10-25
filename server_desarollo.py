from shiny import reactive, render, ui
from funciones.create_param import create_screen
from clases.global_name import global_name_manager
from clases.global_modelo import global_desarollo
from clases.class_extact_time import global_fecha
from funciones.create_nav_menu import create_nav_menu
from clases.class_screens import ScreenClass
from funciones.utils import retornar_card, mover_files
from clases.class_user_proyectName import global_user_proyecto
from funciones.utils import create_modal_parametros, id_buttons_desa
from clases.global_session import global_session
from funciones.utils_2 import get_user_directory
from clases.loadJson import LoadJson

def server_desarollo(input, output, session, name_suffix):
    directorio_desarollo = reactive.value("")
    screen_instance = reactive.value(None)  # Mantener screen_instance como valor reactivo

    def see_session():
        @reactive.effect
        def enviar_session():
            if global_session.proceso.get():
                state = global_session.session_state.get()
                if state["is_logged_in"]:
                    user_id = state["id"]
                    user = get_user_directory(user_id)
                    print(user)
                    user_id_cleaned = user_id.replace('|', '_')
                    directorio_desarollo.set(user)
                    global_desarollo.script_path = f"./Modelar.sh datos_entrada_{user_id_cleaned} datos_salida_{user_id_cleaned}"
                    
                    ##voy a usar la clase como efecto reactivo, ya que si queda encapsulada dentro de la funcion no la podria usar
                    screen_instance.set(ScreenClass(directorio_desarollo.get(), name_suffix))

   ##llamo funcion
    see_session()

    name = "desarrollo"
    count = reactive.value(0)

    @output
    @render.text
    def nombre_proyecto_desarrollo():
        return f'Proyecto: {global_user_proyecto.mostrar_nombre_proyecto_como_titulo()}'

    @output
    @render.ui
    def conten_nav():
        return create_nav_menu(name_suffix, name)

    @reactive.Effect
    @reactive.event(input.file_desarollo)
    async def cargar_Datos_desarrollo():
        await screen_instance.get().load_data(input.file_desarollo, input.delimiter_desarollo, name_suffix)

    @output
    @render.ui
    def error_in_desarollo():
        return screen_instance.get().mensaje_Error.get()

    @output
    @render.data_frame
    def summary_data_validacion_in_sample():
        return screen_instance.get().render_data_summary()

    @output(id=f"summary_data_{name_suffix}")
    @render.data_frame
    def summary_data_desarollo():
        return screen_instance.get().render_data_summary()

    @output
    @render.ui
    def screen_content_desarollo():
        return create_screen(name_suffix)

    @output
    @render.ui
    def card_desarollo2():
        return retornar_card(
            get_file_name=global_name_manager.get_file_name_desarrollo,
            get_fecha=global_fecha.get_fecha_desarrollo,
            modelo=global_desarollo
        )

    @output
    @render.text
    def mensaje_desarrollo():
        return global_desarollo.mostrar_mensaje()

    @ui.bind_task_button(button_id="execute_desarollo")
    @reactive.extended_task
    async def ejectutar_desarrollo_asnyc(click_count, mensaje, proceso):
        await global_desarollo.ejecutar_proceso_prueba(click_count, mensaje, proceso)

    @reactive.effect
    @reactive.event(input.execute_desarollo, ignore_none=True)
    async def ejecutar_desarrollo():
        click_count_value = global_desarollo.click_counter.get()  # Obtener contador
        mensaje_value = global_desarollo.mensaje.get()  # Obtener mensaje actual
        proceso = global_desarollo.proceso.get()
        print(click_count_value)
        ejectutar_desarrollo_asnyc(click_count_value, mensaje_value, proceso)  # Asegúrate de usar await aquí
        fecha_hora_registrada = global_desarollo.log_fecha_hora()
        global_fecha.set_fecha_desarrollo(fecha_hora_registrada)

    @reactive.effect
    @reactive.event(input[f'open_html_{global_desarollo.nombre}'])
    def enviar_result():
        create_navigation_handler(f'open_html_{global_desarollo.nombre}', 'Screen_Resultados')
        ui.update_navs("Resultados_nav", selected="desarrollo")

    def create_modals(id_buttons_desa):
        for id_button in id_buttons_desa:
            @reactive.Effect
            @reactive.event(input[id_button])
            def monitor_clicks(id_button=id_button):
                count.set(count() + 1)	
                if count.get() > 0:
                    print(id_button, count.get())
                    modal = create_modal_parametros(id_button)
                    ui.modal_show(modal)

    create_modals(id_buttons_desa)

    def create_navigation_handler(input_id, screen_name):
        @reactive.Effect
        @reactive.event(input[input_id])
        async def navigate():
            await session.send_custom_message('navigate', screen_name)

    create_navigation_handler('start_desarrollo', 'Screen_User')
    create_navigation_handler('screen_in_sample_desarrollo', 'screen_in_sample')
    create_navigation_handler('screen_Desarollo_desarrollo', 'Screen_Desarollo')
    create_navigation_handler('load_Validacion_desarrollo', 'Screen_valid')
    create_navigation_handler('screen_Produccion_desarrollo', 'Screen_Porduccion')
    create_navigation_handler("ir_modelos_desarrollo", "Screen_3")
    create_navigation_handler("ir_result_desarrollo", "Screen_Resultados")
    create_navigation_handler("volver_etapas_desde_desarrollo", "Screen_User")
