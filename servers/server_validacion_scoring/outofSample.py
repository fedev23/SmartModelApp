from shiny import reactive, render, ui
from funciones.create_param import create_screen
from clases.class_screens import ScreenClass
from global_var import global_data_loader_manager
from funciones.utils_2 import errores, get_user_directory, get_datasets_directory
from clases.global_modelo import modelo_of_sample
from clases.global_session import global_session
from api.db import *
from funciones_modelo.global_estados_model import global_session_modelos
from funciones_modelo.help_models import *
from clases.reactives_name import global_names_reactivos
from global_names import global_name_out_of_Sample
from clases.global_sessionV2 import *
from funciones.validacionY_Scoring.create_card import crate_file_input_y_seleccionador
from clases.global_modelo import modelo_of_sample
from datetime import datetime
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
        valid = validar_existencia_modelo(
            modelo_of_sample.pisar_el_modelo_actual.get(),
            base_datos="Modeling_App.db",
            version_id=global_session.get_id_version(),
            nombre_modelo=modelo_of_sample.nombre,
            nombre_version=global_session.get_versiones_name()
        )
        
        if modelo_of_sample.pisar_el_modelo_actual.get() or valid:
            try:
                path_datos_entrada = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_entrada_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}'
                print(path_datos_entrada, "viendo path de entrada")
                
                origen_modelo_puntoZip = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}'
                
                # Mover archivo .zip y verificar si existe
                zip_existe = mover_file_reportes_puntoZip(origen_modelo_puntoZip, path_datos_entrada)
                if not zip_existe:
                    raise ValueError(f"Es de carácter obligatorio que se ejecute posteriormente la muestra de Desarrollo, para continuar en {global_name_out_of_Sample}")
                
                # Validar si el JSON existe y detenerse si no existe
                path_niveles_sc = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_entrada_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}/version_parametros_{global_session.get_version_parametros_id()}_{global_session.get_versiones_parametros_nombre()}'
                json_existe = help_versios.copiar_json_si_existe(path_niveles_sc, path_datos_entrada)
                if not json_existe:
                    raise ValueError("Hubo un error con los parámetros de ejecución.")
                
                # Verificar si el JSON existe
                path_niveles_sc = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_entrada_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}/version_parametros_{global_session.get_version_parametros_id()}_{global_session.get_versiones_parametros_nombre()}'
                json_existe = help_versios.copiar_json_si_existe(path_niveles_sc, path_datos_entrada)
                
                # Validar existencia de .zip y JSON
               
                # Continuar con la ejecución
                data_Set = get_datasets_directory(global_session.get_id_user(), global_session.get_id_proyecto(), global_session.get_name_proyecto())
                mover_y_renombrar_archivo(global_session_V2.get_nombre_dataset_validacion_sc(), data_Set, name_suffix, path_datos_entrada)
                
                modelo_of_sample.script_path = f'./Validar_Nueva.sh --input-dir {path_datos_entrada} --output-dir {origen_modelo_puntoZip}'
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
                agregar_datos_model_execution(global_session.get_id_version(), modelo_of_sample.nombre, base_datos , "Exito")
                estado_out_sample , hora_of_sample = procesar_etapa(base_datos="Modeling_App.db", id_version=global_session.get_id_version(), etapa_nombre=modelo_of_sample.nombre)
                global_session_modelos.modelo_of_sample_estado.set(estado_out_sample)
                global_session_modelos.modelo_of_sample_hora.set(hora_of_sample)
                modelo_of_sample.proceso_ok.set(False)
            
                
            if modelo_of_sample.proceso_fallo.get():
                agregar_datos_model_execution(global_session.get_id_version(), modelo_of_sample.nombre, "Modeling_App.db", "Error")
                estado_out_sample , hora_of_sample = procesar_etapa(base_datos="Modeling_App.db", id_version=global_session.get_id_version(), etapa_nombre=modelo_of_sample.nombre)
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
    