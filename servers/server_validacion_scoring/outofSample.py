from shiny import reactive, render, ui
from funciones.create_param import create_screen
from clases.class_screens import ScreenClass
from clases.class_user_proyectName import global_user_proyecto
from global_var import global_data_loader_manager
from funciones.utils_2 import errores, get_user_directory, get_datasets_directory_data_set_versiones
from clases.global_modelo import modelo_of_sample
from clases.global_session import global_session
from api.db import *

from funciones_modelo.global_estados_model import global_session_modelos
from funciones_modelo.help_models import *
from clases.reactives_name import global_names_reactivos
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
    def nombre_proyecto_validacion():
        return f'Proyecto: {global_user_proyecto.mostrar_nombre_proyecto_como_titulo(global_session.proyecto_seleccionado())}'

   


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
        if not validar_existencia_modelo("Modeling_App.db", global_session.get_id_version(), modelo_of_sample.nombre, global_session.get_versiones_name()):
            return
        
        try:
            path_datos_entrada = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_entrada_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}'
            origen_modelo_puntoZip =  f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}'
            ##MUEVO EL MODELO .ZIP QUE GENERO DESARROLO PARA QUE PUEDA SER USADO, ESTO DEBERIA SER USANDO EN TODAS LAS ISTANCIAS DE LOS MODELOS
            mover_file_reportes_puntoZip(origen_modelo_puntoZip,path_datos_entrada )
            
            data_Set  = get_datasets_directory_data_set_versiones(global_session.get_id_user(), global_session.get_id_proyecto(), global_session.get_name_proyecto(), global_session.get_versiones_name(), global_session.get_id_version())
       
            mover_y_renombrar_archivo(global_names_reactivos.get_name_file_db(), data_Set, name_suffix, path_datos_entrada)
                    
            #mover_y_renombrar_archivo(global_session_V2.get_nombre_dataset_validacion_sc(), global_session.get_path_guardar_dataSet_en_proyectos(), name_suffix, path_datos_entrada)
                
            path_niveles_sc = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_entrada_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}/version_parametros_{global_session.get_version_parametros_id()}_{global_session.get_versiones_parametros_nombre()}'
            
            help_versios.copiar_json_si_existe(path_niveles_sc, path_datos_entrada)
            modelo_of_sample.script_path = f'./Validar_Nueva.sh --input-dir {path_datos_entrada} --output-dir {origen_modelo_puntoZip}'
            #./Validar_Nueva.sh --input-dir <dir_in> [--output-dir <dir_out>] [--quick <true/false>] [--help]
            ejecutar_of_to_sample(click_count_value, mensaje_value, proceso)
            #insert_table_model(global_session.get_id_user(), global_session.get_id_proyecto(), name_suffix, global_name_manager.get_file_name_validacion())
            if proceso:
                    estado = insert_table_model(global_session.get_id_user(), global_session.get_id_proyecto(), datetime.now().strftime("%Y-%m-%d %H:%M"), modelo_of_sample.nombre, global_names_reactivos.get_name_file_db(), global_session.get_id_version(), 'out_to_sample', 'completado')
                    print(f'estado de la ejecucion {estado}')
            else:
                    estado = insert_table_model(global_session.get_id_user(), global_session.get_id_proyecto(), datetime.now().strftime("%Y-%m-%d %H:%M"), modelo_of_sample.nombre, global_names_reactivos.get_name_file_db(), global_session.get_id_version(), 'out_to_sample', 'error')
                    print(f'estado de la ejecucion {estado}')
                
            
        except Exception as e:
            mensaje.set(f"Primero ejecutar el proceso de Desarrollo para poder ejecutar el proceso  full {str(e)}")
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
    @reactive.event(input.cancel_overwrite_of_Sample)
    def validacion_out_to_Sample_model_run():
         return  ui.modal_remove()
        
    
