from shiny import reactive, render, ui
from funciones.create_param import create_screen
from funciones.create_nav_menu import create_nav_menu
from clases.class_screens import ScreenClass
from clases.class_user_proyectName import global_user_proyecto
from global_var import global_data_loader_manager
from funciones.utils_2 import errores, validar_proyecto, get_user_directory
from clases.global_modelo import modelo_of_sample
from clases.global_session import global_session
from api.db import *
from clases.global_name import global_name_manager
from clases.reactives_name import global_names_reactivos
from funciones.utils import retornar_card



def server_out_of_sample(input, output, session, name_suffix):
    # Obtener el loader de datos desde el manage
    proceso_a_completado = reactive.Value(False)
    directorio = reactive.Value("")
    screen_instance = reactive.Value(None)
    mensaje = reactive.Value("")
    name = "Out-Of-Sample"
    global_names_reactivos.name_validacion_of_to_sample_set(name_suffix)
    data_loader = global_data_loader_manager.get_loader(name_suffix)
    validadacion_retornar_card = reactive.Value("")
    

    # Instanciamos la clase ScreenClass
    #screen_instance = ScreenClass(directorio_validacion, name_suffix)
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
                    modelo_of_sample.script_path = f"./Validar_Nueva.sh datos_entrada_{user_id_cleaned} datos_salida_{user_id_cleaned}"
                    ##voy a usar la clase como efecto reactivo, ya que si queda encapsulada dentro de la funcion no la podria usar
                    screen_instance.set(ScreenClass(directorio.get(), name_suffix))
    
    see_session()
    
   
    @output
    @render.text
    def nombre_proyecto_validacion():
        return f'Proyecto: {global_user_proyecto.mostrar_nombre_proyecto_como_titulo(global_session.proyecto_seleccionado())}'

  

    @output
    @render.ui
    def nav_out_to_sample():
        return create_nav_menu(name_suffix, name)

    @reactive.Effect
    @reactive.event(input.file_validation)
    async def loadOutSample():
        print("entre")
        await screen_instance.get().load_data(input.file_validation, name_suffix)

    @reactive.Effect
    @reactive.event(input[f'load_param_{name_suffix}'])
    def desarollo_out_to_and_valid():
        # 1. Validar si el dataset está cargado
        df = data_loader.getDataset()
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
            #create_navigation_handler(f'load_param_{name_suffix}', 'Screen_3')
            ui.update_accordion("my_accordion", show=["out_to_sample"])


    @output
    @render.text
    def error_in_validacion():
        return errores(mensaje)

    @output
    @render.data_frame
    def summary_data_validacion_out_to_sample():
        return screen_instance.get().render_data_summary()

    # retorno funcion de parametros
    @output
    @render.ui
    def screen_content():
        return create_screen(name_suffix)
    
    
      ##USO ESTE DECORADOR PARA CORRER EL PROCESO ANSYC Y NO HAYA INTERRUCIONES EN EL CODIGO LEER DOCUENTACION
    #https://shiny.posit.co/py/docs/nonblocking.html
    @ui.bind_task_button(button_id="execute_of_sample")
    @reactive.extended_task
    async def ejecutar_of_to_sample(click_count, mensaje, proceso):
        # Llamamos al método de la clase para ejecutar el proceso
        await modelo_of_sample.ejecutar_proceso_prueba(click_count, mensaje, proceso)
        
    ##Luego utilizo el input del id del boton para llamar ala funcion de arriba y que se ejecute con normalidad
    @reactive.Effect
    @reactive.event(input.execute_of_sample, ignore_none=True)
    def validacion_out_to_Sample_model_run():
        click_count_value = modelo_of_sample.click_counter.get()  # Obtener contador
        mensaje_value = modelo_of_sample.mensaje.get()  # Obtener mensaje actual
        proceso = modelo_of_sample.proceso.get()
        ejecutar_of_to_sample(click_count_value, mensaje_value, proceso)
        insert_table_model(global_session.get_id_user(), global_session.get_id_proyecto(), name_suffix, global_name_manager.get_file_name_validacion())
        
        
    @reactive.Effect
    @reactive.event(input[f'open_html_{modelo_of_sample.nombre}'])
    def enviar_result():
        ui.update_navs("Resultados_nav", selected="out_to_sample",)
        
    ##ESTA PARTE VA ESAR DEDICADA A LA LOGICA DE SI EN LA SCREEN SELCCIONO  out_to_sample MANEJARLA ADECUADAMENTE
    
    
    @reactive.Effect
    @reactive.event(input.radio_models)
    def seleccionador_de_radio_button():
        input_radio = input.radio_models()
        validadacion_retornar_card.set(input_radio)
        
        
    @output
    @render.ui
    def card_out_to_sample():
        if validadacion_retornar_card.get()== "1":
            return  retornar_card(
            get_file_name=global_name_manager.get_file_name_validacion(),
            #get_fecha=global_fecha.get_fecha_of_to_Sample,
            modelo=modelo_of_sample)
        else:
              return ui.div()
            
    
    
    @output
    @render.text
    def mensaje_of_sample():
        return modelo_of_sample.mostrar_mensaje()
