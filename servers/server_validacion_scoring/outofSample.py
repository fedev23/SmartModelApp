from shiny import reactive, render, ui
from funciones.create_param import create_screen
from clases.class_screens import ScreenClass
from global_var import global_data_loader_manager
from funciones.utils_2 import *
from clases.global_modelo import modelo_of_sample
from clases.global_session import global_session
from api.db import *
from clases.global_sessionV3 import *
from funciones_modelo.global_estados_model import global_session_modelos
from funciones_modelo.help_models import *
from funciones_modelo.bd_tabla_validacion_sc import *
from clases.reactives_name import global_names_reactivos
from global_names import global_name_out_of_Sample, global_name_in_Sample
from clases.global_sessionV2 import *
from funciones.validacionY_Scoring.create_card import crate_file_input_y_seleccionador
from clases.global_modelo import modelo_of_sample
from datetime import datetime
from clases.class_validacion import Validator
from funciones_modelo.warning_model import *
from funciones.utils import mover_file_reportes_puntoZip
from logica_users.utils  import help_versios 
from funciones.cargar_archivosNEW import mover_y_renombrar_archivo
from funciones_modelo.global_estados_model import global_session_modelos
from funciones_modelo.help_models import *




def server_out_of_sample(input, output, session, name_suffix):
    # Obtener el loader de datos desde el manage
    directorio = reactive.Value("")
    screen_instance = reactive.Value(None)
    mensaje = reactive.Value("")
    name = "Out-Of-Sample"
    click =  reactive.Value(0)
    global_names_reactivos.name_validacion_of_to_sample_set(name_suffix)
    data_loader = global_data_loader_manager.get_loader(name_suffix)
    

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
    def error_in_validacion():
        return errores(mensaje)

    
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
        
        
        id_version_score = insert_validation_scoring(global_session_V2.nombre_dataset_validacion_sc(), global_session.get_version_parametros_id(), modelo_of_sample.nombre)
        
        global_session_V3.id_validacion_scoring.set(id_version_score)
        validar_ids = check_if_exist_id_version_id_niveles_scord(global_session.get_id_version(), global_session.get_version_parametros_id())
        if validar_ids:
            ui.modal_show(create_modal_generic("boton_advertencia_ejecute_of", f"Es obligatorio generar una versión de {global_name_out_of_Sample} y una versión para continuar."))
            return

        valid = validar_existencia_modelo(
            modelo_of_sample.pisar_el_modelo_actual.get(),
            base_datos="Modeling_App.db",
            id_validacion_sc=global_session_V3.id_validacion_scoring.get(),
            nombre_modelo=modelo_of_sample.nombre,  
            nombre_version=global_session.get_versiones_parametros_nombre()
        )
        
        if valid is False:
            ui.modal_show(create_modal_generic("modal_existe_of", "Ya hay un modelo Full generado."))
            return 
        
        if modelo_of_sample.pisar_el_modelo_actual.get() or valid:
            print("estoy pasando este if?")
            validator = Validator(input, global_session.get_data_set_reactivo(), name_suffix)
            try:
                
                input_target_of_sample = input['selectize_columnas_target']()
                print(input_target_of_sample)
                #input_target_of_sample = cambiarAstring(input_target_of_sample)
                validator.validate_target_column_of_sample(input_target_of_sample)
                
                error_messages = validator.get_errors()
                # Si hay errores, mostrar el mensaje y detener el proceso
                if error_messages:
                    mensaje.set("\n".join(error_messages))
                    return  # Detener ejecución si hay errores
                
                origen_modelo_puntoZip = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}/version_parametros_{global_session.get_version_parametros_id()}_{global_session.get_versiones_parametros_nombre()}'
                path_datos_entrada = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_entrada_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}'
                print(f"path_datos_entrada: {path_datos_entrada}")
                
                ##PUNTO ZIP QUE QUEDO DEPRECADO YA QUE SIEMPRE SE VA A OBLIGAR AL USER A EJECUTAR IN SAMPLE
                #origen_modelo_puntoZip = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}'
                print(f"origen_modelo_puntoZip: {origen_modelo_puntoZip}")
                # Mover archivo .zip y verificar si existe
                zip_existe = mover_file_reportes_puntoZip(origen_modelo_puntoZip, path_datos_entrada)
                if not zip_existe:
                    raise ValueError(f"Es de carácter obligatorio que se ejecute posteriormente la muestra de Desarrollo y {global_name_in_Sample}, para continuar en {global_name_out_of_Sample}")
                
                # Validar si el JSON existe y detenerse si no existe
                path_niveles_sc = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_entrada_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}/version_parametros_{global_session.get_version_parametros_id()}_{global_session.get_versiones_parametros_nombre()}'
                json_existe = help_versios.copiar_json_si_existe(path_niveles_sc, path_datos_entrada)
                if not json_existe:
                    raise ValueError("Hubo un error con los parámetros de ejecución.")
                
                # Continuar con la ejecución
                ##MOVILIZAR EL DATASET DEPENDE DONDE SE GUARDA
                data_Set = get_datasets_directory(global_session.get_id_user(), global_session.get_id_proyecto(), global_session.get_name_proyecto())
                mover_y_renombrar_archivo(global_session_V2.get_nombre_dataset_validacion_sc(), data_Set, name_suffix, path_datos_entrada)
                
                path_datos_salida_path  = get_folder_directory_data_validacion_scoring_SALIDA(global_session.get_id_user(), global_session.get_id_proyecto(), global_session.get_name_proyecto(), global_session.get_versiones_name(), global_session.get_id_version(), global_session.get_version_parametros_id(), global_session.get_versiones_parametros_nombre(), global_session_V2.nombre_file_sin_extension_validacion_scoring.get())
                
                if path_datos_salida_path is None:
                    entrada, salida = crear_carpeta_validacion_scoring(global_session.get_id_user(), global_session.get_id_proyecto(), global_session.get_id_version(), global_session.get_version_parametros_id(), global_session.get_versiones_parametros_nombre(), global_session.get_name_proyecto(), global_session.get_versiones_name(), global_session_V2.nombre_file_sin_extension_validacion_scoring.get())
                    path_datos_salida_path = salida
                    
                print(f"datos salida? {path_datos_salida_path}")
                modelo_of_sample.porcentaje_path = path_datos_salida_path
                
                modelo_of_sample.script_path = f'./Validar_Nueva.sh --input-dir {path_datos_entrada} --output-dir {path_datos_salida_path}'
                click.set(click() + 1)
                ejecutar_of_to_sample(click_count_value, mensaje_value, proceso)
                modelo_of_sample.pisar_el_modelo_actual.set(False)
            
            except Exception as e:
                    mensaje.set(f"Error durante la ejecución: {str(e)}")
                    return
    
    
    def agregar_reactivo():  
        @reactive.effect
        def insert_data_depends_value():
            base_datos = "Modeling_App.db"
            if modelo_of_sample.proceso_ok.get():
                print("no falle")
                agregar_datos_model_execution_por_id_validacion_scoring(global_session_V3.id_validacion_scoring.get(),  modelo_of_sample.nombre, global_session_V2.get_nombre_dataset_validacion_sc(), estado="Éxito")
                estado_out_sample , hora_of_sample = procesar_etapa_validacion_scroing(base_datos="Modeling_App.db", id_validacion_sc=global_session_V3.id_validacion_scoring.get(), etapa_nombre=modelo_of_sample.nombre)
                print(f"estado_out_sample {estado_out_sample}, hora_of_sample: {hora_of_sample}")
                global_session_modelos.modelo_of_sample_estado.set(estado_out_sample)
                global_session_modelos.modelo_of_sample_hora.set(hora_of_sample)
                modelo_of_sample.proceso_ok.set(False)
            
                
            if modelo_of_sample.proceso_fallo.get():
                agregar_datos_model_execution_por_id_validacion_scoring(global_session_V3.id_validacion_scoring.get(), modelo_of_sample.nombre, global_session_V2.get_nombre_dataset_validacion_sc(), estado="Error")
                estado_out_sample , hora_of_sample = procesar_etapa_validacion_scroing(base_datos="Modeling_App.db", id_validacion_sc=global_session_V3.id_validacion_scoring.get(), etapa_nombre=modelo_of_sample.nombre)
                print(f"estado_out_sample {estado_out_sample}, hora_of_sample: {hora_of_sample}")
                global_session_modelos.modelo_of_sample_estado.set(estado_out_sample)
                global_session_modelos.modelo_of_sample_hora.set(hora_of_sample)
                modelo_of_sample.proceso_fallo.set(False)
            
    agregar_reactivo()
        
    
    @output
    @render.text
    def mensaje_of_sample():
        return modelo_of_sample.mostrar_mensaje()
    
    
    
    @reactive.Effect
    @reactive.event(input.cancel_overwrite_of_sample)
    def validacion_out_to_Sample_model_run():
         return  ui.modal_remove()
        
    

    
    @reactive.Effect
    @reactive.event(input["continuar_no_overwrite_of_sample"])
    def valid_model_of_sample():
        modelo_of_sample.pisar_el_modelo_actual.set(True)
        return  ui.modal_remove()
    
    
    
    @reactive.calc
    def leer_archivo():
        """Lee el archivo de progreso y actualiza la UI."""
        if click.get() < 1:
            return "Esperando inicio..."

        path_datos_salida  = get_folder_directory_data_validacion_scoring_SALIDA(global_session.get_id_user(), global_session.get_id_proyecto(), global_session.get_name_proyecto(), global_session.get_versiones_name(), global_session.get_id_version(), global_session.get_version_parametros_id(), global_session.get_versiones_parametros_nombre(), global_session_V2.nombre_file_sin_extension_validacion_scoring.get())
        
        name_file = "progreso.txt"

        # Obtener el último porcentaje del archivo
        ultimo_porcentaje = monitorizar_archivo(path_datos_salida, nombre_archivo=name_file)

        if ultimo_porcentaje == "100%":  # Si ya llegó al 100%, detener actualización
            print("Proceso completado. No se seguirá actualizando.")
            return "100%"

        # Actualizar variable reactiva
        modelo_of_sample.file_reactivo.set((ultimo_porcentaje))
        print(f"Último porcentaje capturado: {modelo_of_sample.file_reactivo.get()}")

        # Reactivar cada 3 segundos si aún no ha llegado al 100%
        reactive.invalidate_later(3)

        return ultimo_porcentaje

    # Mostrar el contenido del archivo en la UI
    @render.ui
    def value_of_sample():
        """Muestra el contenido actualizado del archivo en la UI."""
        return f"Última línea: {leer_archivo()}"
    
    
    @reactive.effect
    @reactive.event(input.modal_existe_of)
    def close_modal():
        return ui.modal_remove()
    