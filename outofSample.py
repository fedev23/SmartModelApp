from shiny import reactive, render, ui
from funciones.create_param import create_screen
from funciones.create_nav_menu import create_nav_menu
from clases.class_screens import ScreenClass
from clases.class_user_proyectName import global_user_proyecto
from global_var import global_data_loader_manager
from funciones.utils_2 import errores, validar_proyecto, get_user_directory, render_data_summary
from clases.global_modelo import modelo_of_sample
from clases.global_session import global_session
from api.db import *
from clases.global_name import global_name_manager
from clases.reactives_name import global_names_reactivos
from funciones.utils import retornar_card
from shiny.types import FileInfo
from datetime import datetime
from funciones.funciones_cargaDatos import guardar_archivo
from funciones.help_versios import obtener_opciones_versiones, obtener_ultimo_id_version, obtener_ultimo_nombre_archivo
from clases.global_sessionV2 import *
from funciones.utils_2 import leer_dataset
from funciones.validacionY_Scoring.create_card import crate_file_input_y_seleccionador
import pandas as pd
from funciones.funciones_user import button_remove, create_modal_v2
from clases.global_modelo import modelo_of_sample


def server_out_of_sample(input, output, session, name_suffix):
    # Obtener el loader de datos desde el manage
    dataSet_predeterminado_parms = reactive.Value(None)
    directorio = reactive.Value("")
    screen_instance = reactive.Value(None)
    mensaje = reactive.Value("")
    name = "Out-Of-Sample"
    global_names_reactivos.name_validacion_of_to_sample_set(name_suffix)
    data_loader = global_data_loader_manager.get_loader(name_suffix)
    validadacion_retornar_card = reactive.Value("")
    data_predeterminado = reactive.Value("")
    files_name  = reactive.Value("")
    lista = reactive.Value("")
    reactivo_dinamico = reactive.Value("")
    
    

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
    @render.ui
    def retornar_carga_file_y_seleccionador(): 
        if global_session.get_id_user():
            return crate_file_input_y_seleccionador()
   
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
        try:
            file: list[FileInfo] | None = input.file_validation()
            if not file:
                raise ValueError("No se recibió ningún archivo para validar.")

            print(file, "estoy en fila")
            input_name = file[0]['name']
            print(f"Nombre del archivo recibido: {input_name}")

            # Guardar el archivo
            name_suffix = "_validation"  # Ejemplo de sufijo, ajusta según sea necesario
            ruta_guardado = await guardar_archivo(input.file_validation, name_suffix)
            print(f"El archivo fue guardado en {ruta_guardado}")

            # Obtener fecha actual
            fecha_de_carga = datetime.now().strftime("%Y-%m-%d %H:%M")

            # Insertar datos en la tabla
            id = insert_into_table(
                "validation_scoring",
                ['nombre_archivo_validation_sc', 'fecha_de_carga', 'project_id', 'version_id'],
                [input_name, fecha_de_carga, global_session.get_id_proyecto(), global_session.get_id_version()]
            )
            print("Datos insertados en la tabla validation_scoring.")
            global_session_V2.set_id_Data_validacion_sc(id)
            # Extraer datos
            files_name.set(get_records(
                table='validation_scoring',
                columns=['id_validacion_sc', 'nombre_archivo_validation_sc', 'fecha_de_carga'],
                where_clause='project_id = ?',
                where_params=(global_session.get_id_proyecto(),)
            ))
            # Actualizar opciones y seleccionar predeterminados
            global_session_V2.set_opciones_name_dataset_Validation_sc(obtener_opciones_versiones(files_name.get(), "id_validacion_sc", "nombre_archivo_validation_sc"))
            data_predeterminado.set(obtener_ultimo_id_version(files_name.get(), "id_validacion_sc"))
            
            
            ui.update_select(
                "files_select_validation_scoring",
                choices=global_session_V2.get_opciones_name_dataset_Validation_sc(),
                selected=data_predeterminado.get()
            )
            print("Opciones y selección actualizadas correctamente.")

        except Exception as e:
            # Manejar errores y notificar al usuario
            error_message = f"Error en loadOutSample: {e}"
            #ui.update_text("error_message", error_message)  # Asume que hay un output de texto para mostrar errores
            print(error_message)
    
      

    @reactive.Effect
    @reactive.event(input.files_select_validation_scoring)
    def seleccionador():
        #PREPARO LA CONSULTA
        data_id = input.files_select_validation_scoring()  # Captura el ID seleccionado
        global_session_V2.set_id_Data_validacion_sc(data_id)
        base_datos = 'Modeling_App.db'
        tabla = 'validation_scoring'
        columna_objetivo = 'nombre_archivo_validation_sc'
        columna_filtro = 'id_validacion_sc'
        nombre_file = obtener_valor_por_id(base_datos, tabla, columna_objetivo, columna_filtro, global_session_V2.get_id_Data_validacion_sc())
        
        global_session_V2.set_nombre_dataset_validacion_sc(nombre_file)
        
        ##obengo los valores de la tabla
        lista.set(get_records(table='validation_scoring',
                columns=['id_validacion_sc', 'nombre_archivo_validation_sc', 'fecha_de_carga'],
                where_clause='project_id = ?',
                where_params=(global_session.get_id_proyecto(),)))
        
        if global_session_V2.get_nombre_dataset_validacion_sc() is None:
            dataSet_predeterminado_parms.set(obtener_ultimo_nombre_archivo(lista.get()))
        else:
            dataSet_predeterminado_parms.set(global_session_V2.get_nombre_dataset_validacion_sc())
        
        data = leer_dataset(global_session.get_id_user(), global_session.get_id_proyecto(), global_session.get_name_proyecto(), dataSet_predeterminado_parms.get())
        global_session_V2.set_data_set_reactivo_validacion_sc(data)
        ##actualizo el selector de columna target
    
    
    ##BOTON PARA REMOVER DATASET
    @output
    @render.ui
    def remove_dataset_data_alidacionSC():
        lista_2_borrar = (get_records(table='validation_scoring',
            columns=['id_validacion_sc', 'nombre_archivo_validation_sc', 'fecha_de_carga'],
            where_clause='project_id = ?',
            where_params=(global_session.get_id_proyecto(),)))
        #name.set(global_names_reactivos.get_name_file_db())
        #print(lista_2_borrar, "estoy en lista dos de borrar")
        return button_remove(lista_2_borrar, global_session_V2.get_id_Data_validacion_sc(), "id_validacion_sc", name_suffix)
    
    
    @reactive.Effect
    def boton_para_eliminar_name_data_set_validacion_sc():
        eliminar_version_id = f"eliminar_version_{global_session_V2.get_id_Data_validacion_sc()}_{name_suffix}"

        @reactive.Effect
        @reactive.event(input[eliminar_version_id])
        def eliminar_version_id():
            base_datos = 'Modeling_App.db'
            tabla = 'validation_scoring'
            columna_objetivo = 'nombre_archivo_validation_sc'
            columna_filtro = 'id_validacion_sc'
            nombre_version = obtener_valor_por_id(base_datos, tabla, columna_objetivo, columna_filtro, global_session_V2.get_id_Data_validacion_sc())
            #nombre_version = obtener_valor_por_id(global_session.get_id_dataSet())
            create_modal_v2(f"Seguro que quieres eliminar el Dataset {nombre_version}?", "Confirmar", "Cancelar", "confirmar_id_borrar_dataset_validacion_Sc", "cancelar_id_dataSet_validacion_Sc")
    
    @reactive.Effect
    @reactive.event(input["confirmar_id_borrar_dataset_validacion_Sc"])
    def remove_modal_Dataset():
        ui.modal_remove()     
     
     
    @reactive.Effect
    @reactive.event(input.confirmar_id_borrar_dataset_validacion_Sc)
    def remove_versiones_de_parametros():
        eliminar_version("validation_scoring", "id_validacion_sc", global_session_V2.get_id_Data_validacion_sc())
        columnas = ['id_validacion_sc', 'nombre_archivo_validation_sc']
        lista_de_versiones_new = obtener_versiones_por_proyecto(global_session.get_id_proyecto(), columnas, "validation_scoring", "project_id")
        lista.set(lista_de_versiones_new)
        ui.update_select(
            "files_select_validation_scoring",
            choices={str(vers['id_validacion_sc']): vers['nombre_archivo_validation_sc']
                     for vers in lista_de_versiones_new}
        )
        ui.modal_remove()   
  

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
        return render_data_summary(global_session_V2.get_data_reactivo_validacion_sc())

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
        
        #path_datos_entrada = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_entrada_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}'
        #path_datos_salida  = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}'
        path_entrada = obtener_path_por_proyecto_version(global_session.get_id_proyecto(), global_session.get_id_version(), 'entrada')
        path_salida = obtener_path_por_proyecto_version(global_session.get_id_proyecto(), global_session.get_id_version(), 'salida')
        print(path_entrada, "estoy en entrada")
        print(path_salida, "estoy en salida")
        
        modelo_of_sample.script_path = f'./Validar_Nueva.sh "{path_entrada}" {path_salida}'
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
        print(input_radio, "estoy en radio")
        validadacion_retornar_card.set(input_radio)
      
        
        
    @output
    @render.ui
    def card_out_to_sample():
        if validadacion_retornar_card.get()== "1":
            return  retornar_card(
                #prin(get_data_reactivo_validacion_sc)
            get_file_name=global_session_V2.get_nombre_dataset_validacion_sc(),
            #get_fecha=global_fecha.get_fecha_of_to_Sample,
            modelo=modelo_of_sample)
        else:
              return ui.div()
            
    
    @output
    @render.ui
    def seleccionador_target():
        # Reactivo para verificar el valor del radio botón y actualizar dinámicamente
        @reactive.Effect
        def handle_radio_change():
            if validadacion_retornar_card.get() == "1":
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
        if validadacion_retornar_card.get() == "1":
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
    def mensaje_of_sample():
        return modelo_of_sample.mostrar_mensaje()
