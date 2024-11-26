from shiny import reactive, render, ui
import pandas as pd
from api.db import *
from global_var import global_data_loader_manager  # Importar el gestor global
from clases.global_sessionV2 import global_session_V2
from clases.global_name import global_name_manager
from clases.global_modelo import modelo_produccion
from funciones.create_nav_menu import create_nav_menu
from clases.class_screens import ScreenClass
from funciones.utils import retornar_card
from clases.class_user_proyectName import global_user_proyecto
from funciones.utils_2 import errores, validar_proyecto
from clases.global_session import global_session
from funciones.utils_2 import get_user_directory, leer_dataset
from funciones.help_versios import obtener_ultimo_nombre_archivo
from clases.reactives_name import global_names_reactivos

def server_produccion(input, output, session, name_suffix):
    proceso_a_completado = reactive.Value(False)
    directorio = reactive.Value("")
    screen_instance = reactive.Value("")
    name = "Producción"
    global_names_reactivos.name_produccion_set(name_suffix)
    mensaje = reactive.Value("")
    directorio = reactive.Value("")
    lista = reactive.Value(True)
    reactivo_dinamico =  reactive.Value("")
    dataSet_predeterminado_parms =  reactive.Value("")
    
    

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
    
    @reactive.Effect
    @reactive.event(input.radio_models)
    def seleccionador_de_radio_button():
        input_radio = input.radio_models()
        reactivo_dinamico.set(input_radio)
            

    @output
    @render.ui
    def card_produccion1():
        if  reactivo_dinamico.get() == "2":
            return retornar_card(
                get_file_name=global_name_manager.get_file_name_produccion,
                #get_fecha=global_fecha.get_fecha_produccion,
                modelo=modelo_produccion
            )
    
    @output
    @render.ui
    def seleccionador_target():
        # Reactivo para verificar el valor del radio botón y actualizar dinámicamente
        @reactive.Effect
        def handle_radio_change():
            if reactivo_dinamico.get() == "2":
                # Actualiza la lista de registros
                lista.set(get_records(
                    table='validation_scoring',
                    columns=['id_validacion_sc', 'nombre_archivo_validation_sc', 'fecha_de_carga'],
                    where_clause='project_id = ?',
                    where_params=(global_session.get_id_proyecto(),)
                ))

                # Determina el dataset predeterminado o usa uno existente
                if global_session_V2.get_nombre_dataset_validacion_sc() is None:
                    dataSet_predeterminado_parms.set(
                        obtener_ultimo_nombre_archivo(lista.get())
                    )
                else:
                    dataSet_predeterminado_parms.set(
                        global_session_V2.get_nombre_dataset_validacion_sc()
                    )

                # Leer el dataset y actualizar datos globales
                data = leer_dataset(
                    global_session.get_id_user(),
                    global_session.get_id_proyecto(),
                    global_session.get_name_proyecto(),
                    dataSet_predeterminado_parms.get()
                )
                global_session_V2.set_data_set_reactivo_validacion_sc(data)

                # Verificar si el dataset es válido y obtener nombres de columnas
                if isinstance(data, pd.DataFrame) and not data.empty:
                    column_names = data.columns.tolist()
                else:
                    column_names = []

                # Actualizar el selector con las columnas disponibles
                ui.update_selectize("selectize_columnas_target", choices=column_names)

        # Devuelve el selector con opciones dinámicamente actualizadas
        if reactivo_dinamico.get() == "2":
            return ui.input_selectize(
                "selectize_columnas_target",
                "",
                choices=[],
                multiple=False,
                options={"placeholder": "Seleccionar columna target."}
            )
        else:
            return None
        
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
        
   
  