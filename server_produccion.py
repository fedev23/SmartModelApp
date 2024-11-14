from shiny import reactive, render, ui
import pandas as pd
from api.db import *
from global_var import global_data_loader_manager  # Importar el gestor global
from funciones.create_param import create_screen
from clases.global_name import global_name_manager
from clases.global_modelo import modelo_produccion
from funciones.create_nav_menu import create_nav_menu
from clases.class_screens import ScreenClass
from funciones.utils import retornar_card
from clases.class_user_proyectName import global_user_proyecto
from funciones.utils_2 import errores, validar_proyecto
from clases.global_session import global_session
from funciones.utils_2 import get_user_directory
from clases.reactives_name import global_names_reactivos

def server_produccion(input, output, session, name_suffix):
    proceso_a_completado = reactive.Value(False)
    directorio = reactive.Value("")
    screen_instance = reactive.Value("")
    directorio_produccion = r'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat'
    name = "Producción"
    global_names_reactivos.name_produccion_set(name_suffix)
    mensaje = reactive.Value("")
    directorio = reactive.Value("")
    

    @output
    @render.text
    def nombre_proyecto_produccion():
        return f'Proyecto: {global_user_proyecto.mostrar_nombre_proyecto_como_titulo(global_session.proyecto_seleccionado())}'
    
    
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
                    directorio.set(user)
                    modelo_produccion.script_path = f"./Scoring.sh datos_entrada_{user_id_cleaned} datos_salida_{user_id_cleaned}"
                    ##voy a usar la clase como efecto reactivo, ya que si queda encapsulada dentro de la funcion no la podria usar
                    screen_instance.set(ScreenClass(directorio.get(), name_suffix))
                    
    see_session()

   

    @output
    @render.ui
    def nav_out_to_produccion():
        return create_nav_menu(name_suffix, name)

    @reactive.Effect
    @reactive.event(input.file_produccion)
    async def loadOutSample():
        print("entre")
        await screen_instance.get().load_data(input.file_produccion, input.delimiter_produccion, name_suffix)

    @reactive.Effect
    @reactive.event(input.load_param_produccion)
    def produccion_out_to_and_valid():
        df = global_data_loader_manager.getDataset()
        if df is None:
            mensaje.set(f"No se seleccionó ningún archivo en {name}")
            return  # Detener la ejecución si no hay dataset

        # 2. Validar si el proyecto está asignado
        proyecto_nombre = global_session.get_id_user()
        if not validar_proyecto(proyecto_nombre):
            mensaje.set(f"Es necesario tener un proyecto asignado o creado para continuar en {name}")
            return  # Detener la ejecución si no hay proyecto asignado

        # 3. Continuar si ambas validaciones anteriores pasan
        if screen_instance.get().proceso_a_completado.get():
            create_navigation_handler(f'load_param_{name_suffix}', 'Screen_3')
            ui.update_accordion("my_accordion", show=["produccion"])

    @output
    @render.text
    def error_in_produccion():
        return errores(mensaje)

    @output
    @render.data_frame
    def summary_data_produccion():
        return screen_instance.get().render_data_summary()

    @output
    @render.ui
    def mostrarOut_produccion():
        if proceso_a_completado.get():
            return ui.input_action_button("ir_ejecucion_produccion", "Ir a ejecución")
        return ui.TagList()

    # estoy usando la clase para la creacion de modelos aca, lueog veo si adapto todas o las dejo en modelo

    @output
    @render.ui
    def card_produccion1():
        return retornar_card(
            get_file_name=global_name_manager.get_file_name_produccion,
            #get_fecha=global_fecha.get_fecha_produccion,
            modelo=modelo_produccion
        )

    @output
    @render.text
    def mensaje_produccion():
        return modelo_produccion.mostrar_mensaje()


       ##USO ESTE DECORADOR PARA CORRER EL PROCESO ANSYC Y NO HAYA INTERRUCIONES EN EL CODIGO LEER DOCUENTACION
    #https://shiny.posit.co/py/docs/nonblocking.html
    @ui.bind_task_button(button_id="execute_produccion")
    @reactive.extended_task
    async def ejectutar_produccion(click_count, mensaje, proceso):
        # Llamamos al método de la clase para ejecutar el proceso
        await modelo_produccion.ejecutar_proceso_prueba(click_count, mensaje, proceso)
        
    ##Luego utilizo el input del id del boton para llamar ala funcion de arriba y que se ejecute con normalidad
    @reactive.Effect
    @reactive.event(input.execute_produccion, ignore_none=True)
    def validacion_out_to_Sample_model_run():
        click_count_value = modelo_produccion.click_counter.get()  # Obtener contador
        mensaje_value = modelo_produccion.mensaje.get()  # Obtener mensaje actual
        proceso = modelo_produccion.proceso.get()
        ejectutar_produccion(click_count_value, mensaje_value, proceso)
        insert_table_model(global_session.get_id_user(), global_session.get_id_proyecto(), name_suffix, global_name_manager.get_file_name_produccion())
        
        

    def create_navigation_handler(input_id, screen_name):
        @reactive.Effect
        @reactive.event(input[input_id])
        async def navigate():
            await session.send_custom_message('navigate', screen_name)

    @reactive.Effect
    @reactive.event(input[f'open_html_{modelo_produccion.nombre}'])
    def enviar_result():
        create_navigation_handler(
            f'open_html_{modelo_produccion.nombre}', 'Screen_Resultados')
        ui.update_accordion("my_accordion", show=["produccion"])

    create_navigation_handler('start_produccion', 'Screen_User')
    create_navigation_handler('screen_in_sample_produccion', 'screen_in_sample')
    create_navigation_handler('screen_Desarollo_produccion', 'Screen_Desarollo')
    create_navigation_handler('load_Validacion_produccion', 'Screen_valid')
    create_navigation_handler('screen_Produccion_produccion', 'Screen_Porduccion')
    create_navigation_handler('ir_modelos_produccion', 'Screen_3')
    create_navigation_handler("ir_result_produccion", "Screen_Resultados")
    create_navigation_handler("volver_produccion", "Screen_User")
