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



def server_desarollo(input, output, session, name_suffix):
    directorio_desarollo = r'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_entrada'
    screen_instance = ScreenClass(directorio_desarollo,  name_suffix)
    name = "desarrollo"
    count = reactive.value(0)
    check = reactive.Value(False)
    contar_script = reactive.value(0)


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
        await screen_instance.load_data(input.file_desarollo, input.delimiter_desarollo, name_suffix)
        # screen_instance_in_sample.load_data(input.file_desarollo, input.delimiter_desarollo,name_suffix)

    # FIJARME SI LA MANERA DE PENSAR QUE TENGO EN, QUE SIMPLEMENTE EJECUTEN EL MISMO PATH DESAROLLO Y IN SAMPLE PORQUE COMPARTE EL MIMSO DATASET ESTA BIEN
    @output
    @render.ui
    def error_in_desarollo():
        return screen_instance.mensaje_Error.get()

    # Hago dos mimas llamadas ya que validacion in sample y desarollo

    @output
    @render.data_frame
    def summary_data_validacion_in_sample():
        return screen_instance.render_data_summary()

    @output(id=f"summary_data_{name_suffix}")
    @render.data_frame
    def summary_data_desarollo():
        #return render.DataGrid(ejemplo_niveles_riesgo, editable=True, width='500px')
        return screen_instance.render_data_summary()

    # Creo screen para el panel de datos
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

        # USO ESTE DECORADOR PARA CORRER EL PROCESO ANSYC Y NO HAYA INTERRUCIONES EN EL CODIGO LEER DOCUENTACION
    # https://shiny.posit.co/py/docs/nonblocking.html

    @ui.bind_task_button(button_id="execute_desarollo")
    @reactive.extended_task
    async def ejectutar_desarrollo_asnyc(click_count, mensaje, proceso):
        await global_desarollo.ejecutar_proceso_prueba(click_count, mensaje, proceso)
        # proceso = global_desarollo.proceso.get()
        # print(proceso)

    # Capturamos el evento del botón execute_desarollo y ejecutamos la tarea asincrónica
    @reactive.effect
    @reactive.event(input.execute_desarollo, ignore_none=True)
    def ejecutar_desarrollo():
        click_count_value = global_desarollo.click_counter.get()  # Obtener contador
        mensaje_value = global_desarollo.mensaje.get()  # Obtener mensaje actual
        proceso = global_desarollo.proceso.get()
        ejectutar_desarrollo_asnyc(click_count_value, mensaje_value, proceso)
        fecha_hora_registrada = global_desarollo.log_fecha_hora()
        print("me llevo la fecha o what?")
        global_fecha.set_fecha_desarrollo(fecha_hora_registrada)
        
        

    @reactive.effect
    @reactive.event(input[f'open_html_{global_desarollo.nombre}'])
    def enviar_result():
        create_navigation_handler(f'open_html_{global_desarollo.nombre}', 'Screen_Resultados')
        ui.update_navs("Resultados_nav", selected="desarrollo",)

    def create_modals(id_buttons_desa):
        for id_button in id_buttons_desa:
            # Crear un efecto reactivo para cada botón en la lista
            @reactive.Effect
            @reactive.event(input[id_button])
            # id_button se pasa como argumento con valor predeterminado
            def monitor_clicks(id_button=id_button):
                count.set(count() + 1)
                if count.get() >= 1:
                    print(id_button, count.get())
                    modal = create_modal_parametros(id_button)
                    ui.modal_show(modal)

    # Llamar a la función con la lista de botones
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
