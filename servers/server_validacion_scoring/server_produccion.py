from shiny import reactive, render, ui
import pandas as pd
from api.db import *
from global_var import global_data_loader_manager  # Importar el gestor global
from clases.global_sessionV2 import global_session_V2
from clases.global_name import global_name_manager
from clases.global_modelo import modelo_produccion
from clases.class_screens import ScreenClass
from funciones.utils import retornar_card
from clases.class_user_proyectName import global_user_proyecto
from funciones.utils_2 import errores, validar_proyecto
from clases.global_session import global_session
from funciones.utils_2 import get_user_directory, leer_dataset
from logica_users.utils.help_versios import copiar_json_si_existe
from clases.reactives_name import global_names_reactivos
from funciones.utils import mover_file_reportes_puntoZip
from funciones.cargar_archivosNEW import mover_y_renombrar_archivo
from funciones_modelo.global_estados_model import global_session_modelos
from funciones_modelo.help_models import *


def server_produccion(input, output, session, name_suffix):
    proceso_a_completado = reactive.Value(False)
    directorio = reactive.Value("")
    screen_instance = reactive.Value("")
    name = "Producción"
    global_names_reactivos.name_produccion_set(name_suffix)
    mensaje = reactive.Value("")
    directorio = reactive.Value("")
    
   
    
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
                    ##voy a usar la clase como efecto reactivo, ya que si queda encapsulada dentro de la funcion no la podria usar
                    screen_instance.set(ScreenClass(directorio.get(), name_suffix))
                    
    see_session()

   
    @output
    @render.text
    def error_in_produccion():
        return errores(mensaje)

    @output
    @render.data_frame
    def summary_data_produccion():
        return screen_instance.get().render_data_summary()

    
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
        try:
            path_entrada = obtener_path_por_proyecto_version( global_session.get_id_version(), 'entrada')
            path_salida = obtener_path_por_proyecto_version( global_session.get_id_version(), 'salida')
            
            if not path_entrada or not path_salida:
                raise ValueError("No se pudieron obtener las rutas de entrada y/o salida")
                
            #path_datos_entrada = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_entrada_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}'
            #origen_modelo_puntoZip =  f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}'
            
            path_niveles_sc = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_entrada_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}/version_parametros_{global_session.get_version_parametros_id()}_{global_session.get_versiones_parametros_nombre()}'
            
            copiar_json_si_existe(path_niveles_sc, path_entrada)
            mover_file_reportes_puntoZip(path_salida,path_entrada)
            mover_y_renombrar_archivo(global_session_V2.get_nombre_dataset_validacion_sc(), global_session.get_path_guardar_dataSet_en_proyectos(), name_suffix, path_entrada)
            
            modelo_produccion.script_path = f'./Scoring.sh --input-dir {path_entrada} --output-dir {path_salida}'
            
            ejectutar_produccion(click_count_value, mensaje_value, proceso)
            
        except Exception as e:
            mensaje_value.set(f"Primero ejecutar el proceso de Desarrollo para poder ejecutar el proceso  full {str(e)}")
            return
        
    
    
    def agregar_reactivo():  
        @reactive.effect
        def insert_data_depends_value():
            base_datos = "Modeling_App.db"
            if modelo_produccion.proceso_ok.get():
                agregar_datos_model_execution(global_session.get_id_version(), modelo_produccion.nombre, base_datos , "Exito")
                estado_out_sample , hora_of_sample = procesar_etapa(base_datos="Modeling_App.db", id_version=global_session.get_id_version(), etapa_nombre="of_sample")
                global_session_modelos.modelo_of_sample_estado.set(estado_out_sample)
                global_session_modelos.modelo_of_sample_hora.set(hora_of_sample)
                
            
                
            if modelo_produccion.proceso_fallo.get():
                agregar_datos_model_execution(global_session.get_id_version(), modelo_produccion.nombre, "Modeling_App.db", "Error")
                estado_out_sample , hora_of_sample = procesar_etapa(base_datos="Modeling_App.db", id_version=global_session.get_id_version(), etapa_nombre="of_sample")
                global_session_modelos.modelo_of_sample_estado.set(estado_out_sample)
                global_session_modelos.modelo_of_sample_hora.set(hora_of_sample)
                
    agregar_reactivo()      
    
        
  