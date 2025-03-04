from shiny import reactive, render, ui
from api.db import *
from clases.global_sessionV2 import global_session_V2
from clases.global_modelo import modelo_produccion
from funciones_modelo.warning_model import *
from funciones.utils_2 import errores, get_folder_directory_data_validacion_scoring_SALIDA, crear_carpeta_validacion_scoring
from clases.global_session import global_session
from funciones_modelo.bd_tabla_validacion_sc import *
from clases.global_sessionV3 import *
from funciones.utils_2 import get_user_directory, get_datasets_directory,get_folder_directory_data_validacion_scoring
from logica_users.utils.help_versios import copiar_json_si_existe, func_copiar_files
from logica_users.utils.manejo_session import generar_paths_of_sample_y_scoring, generar_paths_insa
from clases.reactives_name import global_names_reactivos
from global_names import global_name_produccion
from funciones.utils import mover_file_reportes_puntoZip
from funciones.cargar_archivosNEW import mover_y_renombrar_archivo
from funciones_modelo.global_estados_model import global_session_modelos
from funciones_modelo.help_models import *
from api.db.up_date import obtener_ultimo_id_file_scoring
from global_names import global_name_out_of_Sample, global_name_in_Sample
from global_names import global_name_out_of_Sample


def server_produccion(input, output, session, name_suffix):
    global_names_reactivos.name_produccion_set(name_suffix)
    mensaje = reactive.Value("")
    directorio = reactive.Value("")
    click = reactive.Value(0)
    listo_para_ejecutar = reactive.Value(False)
    ultimo_porcentaje = reactive.Value(0)
   
    
    
    @output
    @render.text
    def error_in_produccion():
        return errores(mensaje)

    # estoy usando la clase para la creacion de modelos aca, lueog veo si adapto todas o las dejo en modelo
    
        
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
    

        valid = verificar_estado_modelo_edited('Modeling_App.db', "scoring",  "id_score", global_session_V3.id_score.get(), "id_nombre_file", global_session_V2.get_id_Data_validacion_sc())
        if valid:
            return  ui.modal_show(create_modal_generic("Close_modal_existe_ya_modelo", f"Ya existe un modelo generado para el Dataset: {global_session_V2.get_nombre_dataset_validacion_sc()}"))
        

        validar_ids = check_if_exist_id_version_id_niveles_scord(global_session.get_id_version(), global_session.get_version_parametros_id())
        if validar_ids:
            ui.modal_show(create_modal_generic("boton_advertencia_ejecute_produccion", f"Es obligatorio generar una versión de {global_name_out_of_Sample} y una versión para continuar."))
            return

        
        if modelo_produccion.pisar_el_modelo_actual.get() or valid is False:
            try:
                id_version_score = insert_scoring("scoring" , global_session_V2.nombre_dataset_validacion_sc(), global_session.get_version_parametros_id(), modelo_produccion.nombre)
                global_session_V3.id_score.set(id_version_score)
                
                
                path_datos_entrada = generar_paths_of_sample_y_scoring(global_session, global_session_V2, 'entrada')
                origen_modelo_puntoZip = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}/version_parametros_{global_session.get_version_parametros_id()}_{global_session.get_versiones_parametros_nombre()}'
                
                path_in_sample, insa_salida = generar_paths_insa(global_session)
                ##CHEQUEAR SI TENGO QUE CREAR UN NUEVO LUGAR DE DATOS ENTRADA.
                print(f"path entrada? {path_datos_entrada}")
                
                func_copiar_files(path_in_sample, path_datos_entrada, nombre_archivo="Muestra_Desarrollo.txt")
        
                zip_existe = mover_file_reportes_puntoZip(origen_modelo_puntoZip,path_datos_entrada)
                if not zip_existe:
                     return ui.modal_show(create_modal_generic("boton_advertencia_ejecute_of_inss", f"Es obligatorio generar un modelo de {global_name_in_Sample} para continuar."))

                print("llegue??")
                json_yes = copiar_json_si_existe(path_in_sample, path_datos_entrada)
                if not json_yes:
                    raise ValueError("Hubo un error con los parámetros de ejecución.")
                
               
                
                path_folder_dataset  = get_datasets_directory(global_session.get_id_user(), global_session.get_id_proyecto(), global_session.get_name_proyecto())
        
                mover_y_renombrar_archivo(global_session_V2.get_nombre_dataset_validacion_sc(), path_folder_dataset, name_suffix, path_datos_entrada)
                
                #mover_y_renombrar_archivo(global_session_V2.get_nombre_dataset_validacion_sc(), global_session.get_path_guardar_dataSet_en_proyectos(), name_suffix, path_entrada)
                
                path_datos_salida_path  = get_folder_directory_data_validacion_scoring_SALIDA(global_session.get_id_user(), global_session.get_id_proyecto(), global_session.get_name_proyecto(), global_session.get_versiones_name(), global_session.get_id_version(), global_session.get_version_parametros_id(), global_session.get_versiones_parametros_nombre(), global_session_V2.nombre_file_sin_extension_validacion_scoring.get())
            
                if path_datos_salida_path is None:
                    entrada, salida = crear_carpeta_validacion_scoring(global_session.get_id_user(), global_session.get_id_proyecto(), global_session.get_id_version(), global_session.get_version_parametros_id(), global_session.get_versiones_parametros_nombre(), global_session.get_name_proyecto(), global_session.get_versiones_name(), global_session_V2.nombre_file_sin_extension_validacion_scoring.get())
                    path_datos_salida_path = salida
                
                
                print(f"pat salida antes de correr {path_datos_salida_path}")
                modelo_produccion.porcentaje_path = path_datos_salida_path
                click.set(click() + 1)
                
                print(f"path_datos_salida_path: {path_datos_salida_path}")
                modelo_produccion.script_path = f'./Scoring.sh --input-dir {path_datos_entrada} --output-dir {path_datos_salida_path}'
                listo_para_ejecutar.set(True)
                ejectutar_produccion(click_count_value, mensaje_value, proceso)
                modelo_produccion.pisar_el_modelo_actual.set(False)
            except Exception as e:
                mensaje.set(f"Error durante la ejecución: {str(e)}")
                return
        
    
    
    def agregar_reactivo():  
        @reactive.effect
        def insert_data_depends_value():
            base_datos = "Modeling_App.db"
            if modelo_produccion.proceso_ok.get():
                agregar_datos_model_execution_scoring(global_session_V3.id_score.get(), modelo_produccion.nombre,  global_session_V2.get_id_Data_validacion_sc(), estado="Éxito")
                estado_produccion , hora_produccion, mensaje_error = procesar_etapa_validacion_scroing(base_datos="Modeling_App.db", id_score=global_session_V3.id_score.get(), id_nombre_file=global_session_V2.get_id_Data_validacion_sc(), etapa_nombre=modelo_produccion.nombre)
                global_session_modelos.modelo_produccion_estado.set(estado_produccion)
                global_session_modelos.modelo_produccion_hora.set(hora_produccion)
                modelo_produccion.proceso_ok.set(False)
            
                
            if modelo_produccion.proceso_fallo.get():
                agregar_datos_model_execution_scoring(global_session_V3.id_score.get(), modelo_produccion.nombre, global_session_V2.get_id_Data_validacion_sc(), estado="Error", mensaje_error=modelo_produccion.mensaje.get())
                estado_produccion , hora_produccion, mensaje_error = procesar_etapa_validacion_scroing(base_datos="Modeling_App.db", id_score=global_session_V3.id_score.get(), id_nombre_file=global_session_V2.get_id_Data_validacion_sc(), etapa_nombre=modelo_produccion.nombre)
                global_session_modelos.modelo_produccion_estado.set(estado_produccion)
                global_session_modelos.modelo_produccion_hora.set(hora_produccion)
                global_session_modelos.modelo_produccion_error.set(mensaje_error)
                modelo_produccion.proceso_fallo.set(False),
                
    agregar_reactivo()      
    
        
    
    @reactive.Effect
    @reactive.event(input.cancel_overwrite_produccion)
    def modal_():
         return  ui.modal_remove()
     
    
    
    @reactive.calc
    def leer_archivo():
        if listo_para_ejecutar.get():
            
            """Lee el archivo de progreso y actualiza la UI."""
            if modelo_produccion.proceso_fallo.get():
                return
            
            if click.get() >= 1:
                path_datos_salida  = get_folder_directory_data_validacion_scoring_SALIDA(global_session.get_id_user(), global_session.get_id_proyecto(), global_session.get_name_proyecto(), global_session.get_versiones_name(), global_session.get_id_version(), global_session.get_version_parametros_id(), global_session.get_versiones_parametros_nombre(), global_session_V2.nombre_file_sin_extension_validacion_scoring.get())
                name_file = "progreso.txt"

                # Obtener el último porcentaje del archivo
                ultimo_porcentaje.set(monitorizar_archivo(path_datos_salida, nombre_archivo=name_file)) 
                if ultimo_porcentaje.get() == "100%":  # Si ya llegó al 100%, detener actualización
                    print("Proceso completado. No se seguirá actualizando.")
                    modelo_produccion.eliminar_archivo_progreso(path_datos_salida, name_file)
                    return "100%"

                # Actualizar variable reactiva
                modelo_produccion.file_reactivo.set((ultimo_porcentaje))
                # Reactivar cada 3 segundos si aún no ha llegado al 100%
                reactive.invalidate_later(2)
                
                return ultimo_porcentaje.get()

    # Mostrar el contenido del archivo en la UI
    @render.ui
    def value_produccion():
        if click.get() >= 1:
            return f"Porcentaje: {leer_archivo()}"
    
    @reactive.effect
    @reactive.event(input.boton_advertencia_ejecute_of_inss)
    def name():
      return ui.modal_remove()