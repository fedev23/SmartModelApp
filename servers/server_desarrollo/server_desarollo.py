from shiny import reactive, render, ui
from funciones.create_param import create_screen
from clases.global_modelo import global_desarollo
from clases.class_screens import ScreenClass
from funciones.utils import retornar_card
from clases.class_user_proyectName import global_user_proyecto
from funciones.utils_2 import get_user_directory, render_data_summary, aplicar_transformaciones, mostrar_error, cambiarAstring, trans_nulos_adic, get_datasets_directory, detectar_delimitador
from api.db import *
from clases.global_session import *
from clases.global_sessionV2 import *
from clases.reactives_name import global_names_reactivos
from clases.global_session import *
from clases.class_validacion import Validator
from clases.loadJson import LoadJson
from datetime import datetime
from clases.global_reactives import global_estados
from funciones.cargar_archivosNEW import mover_y_renombrar_archivo
from funciones.clase_estitca.cargar_files import FilesLoad
from clases.reactives_name import global_names_reactivos
from funciones_modelo.global_estados_model import global_session_modelos
from funciones_modelo import help_models
from api.db.sqlite_utils import *
from funciones_modelo.global_estados_model import global_session_modelos
from funciones_modelo.global_estados_model import global_session_modelos
from funciones_modelo.help_models import *


def server_desarollo(input, output, session, name_suffix):
    clase_cargar_files = FilesLoad(name_suffix)
    
    directorio_desarollo = reactive.value("")
    screen_instance = reactive.value(None)  # Mantener screen_instance como valor reactivo
    user_id_send = reactive.Value("")
    global_names_reactivos.name_desarrollo_set(name_suffix)
    mensaje = reactive.Value("")
    
    
    
    # Diccionario de transformaciones
    transformaciones = {
        'par_ids': cambiarAstring,
        'par_target': cambiarAstring,
        'cols_forzadas_a_predictoras': cambiarAstring,
        'par_var_grupo': cambiarAstring,
        'par_weight': cambiarAstring,
        'cols_nulos_adic': trans_nulos_adic,
        'cols_forzadas_a_cat': cambiarAstring,
        'cols_no_predictoras': cambiarAstring
    }


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
                    user_id_send.set(user_id_cleaned)
                    directorio_desarollo.set(user)
                    ##voy a usar la clase como efecto reactivo, ya que si queda encapsulada dentro de la funcion no la podria usar
                    screen_instance.set(ScreenClass(directorio_desarollo.get(), name_suffix))

   ##llamo funcion
    see_session()

    name = "desarrollo"
    count = reactive.value(0)
    
    
   
    @output
    @render.text
    def nombre_proyecto_desarrollo():
        return f'Proyecto: {global_user_proyecto.mostrar_nombre_proyecto_como_titulo(global_session.proyecto_seleccionado())}'

    @reactive.Effect
    @reactive.event(input.file_desarollo)
    async def datos_desarrolo():
        await clase_cargar_files.cargar_Datos_desarrollo(input.file_desarollo)
    
    @reactive.Effect
    @reactive.event(input.cancel_overwrite)
    def overwrite_file():
        return  ui.modal_remove()
            
        
    
    @output
    @render.ui
    def error_in_desarollo():
        return screen_instance.get().mensaje_Error.get()

    @output
    @render.data_frame
    def summary_data_validacion_in_sample():
        return render_data_summary(global_session.get_data_set_reactivo())

    @output(id=f"summary_data_{name_suffix}")
    @render.data_frame
    def summary_data_desarollo():
        return render_data_summary(global_session.get_data_set_reactivo())
        #return screen_instance.get().render_data_summary()

    @output
    @render.ui
    def screen_content_desarollo():
        return create_screen(name_suffix)


    ##CADA FUNCION TIENE UN MODELO ASIGNADO
    @output
    @render.ui
    def card_desarollo2():
        return retornar_card(
            get_file_name=global_names_reactivos.get_name_file_db(),
            fecha=global_session_modelos.modelo_desarrollo_hora.get(),
            estado=global_session_modelos.modelo_desarrollo_estado.get(),
            modelo=global_desarollo
        )

    @output
    @render.text
    def mensaje_desarrollo():
        return global_desarollo.mostrar_mensaje()

    @ui.bind_task_button(button_id="execute_desarollo")
    @reactive.extended_task
    async def ejectutar_desarrollo_asnyc(click_count, mensaje, proceso):
        await global_desarollo.ejecutar_proceso_prueba(click_count, mensaje, proceso)

    @reactive.effect
    @reactive.event(input.execute_desarollo, ignore_none=True)
    async def ejecutar_desarrollo():
        click_count_value = global_desarollo.click_counter.get()  # Obtener contador
        mensaje_value = global_desarollo.mensaje.get()  # Obtener mensaje actual
        proceso = global_desarollo.get_proceso()

        # Crear instancia de la clase Validator
        validator = Validator(input, global_session.get_data_set_reactivo(), name_suffix)

        # Realizar las validaciones
        validator.validate_column_identifiers()
        validator.validate_iv()
        validator.validate_target_column()
        validator.validate_training_split()

        # Obtener los errores de validación
        error_messages = validator.get_errors()

        # Si hay errores, mostrar el mensaje y detener el proceso
        if error_messages:
            mensaje.set("\n".join(error_messages))
            return  # Detener ejecución si hay errores

        # Si no hay errores, limpiar el mensaje y proceder
        mensaje.set("")  # Limpia el mensaje de error

        # Procesar los inputs y aplicar las transformaciones
        inputs_procesados = aplicar_transformaciones(input, transformaciones)
        
        # Guardar los inputs procesados en un archivo JSON
        if global_session.proceso.get():
            state = global_session.session_state.get()
            if state["is_logged_in"]:
                user_id = state["id"]
                user_id_cleaned = user_id.replace('|', '_')
                json_loader = LoadJson(input) 
                json_loader.inputs.update(inputs_procesados)
                #ACTUALIZO VARIOS INPUTS QUE SON DINAMICOS CON EL FIN DE QUE NO ESTEN NULOS EN LA LLAMADA AL JSON
                json_loader.inputs['delimiter_desarollo'] = global_estados.get_delimitador()
                json_loader.inputs['proyecto_nombre'] = global_session.get_name_proyecto() 
                json_loader.inputs['file_desarollo'] = global_names_reactivos.get_name_file_db()
                json_file_path = json_loader.loop_json()
                print(f"Inputs guardados en {json_file_path}")
            ##Y NO LO PUEDO PONER CON ESPACIO O CON OS.JION POR QUE ME GENERA / DONDE NO VAN
                path_datos_entrada = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_entrada_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}'
                path_datos_salida  = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}'
                
                
                ##CARGO EL PATH VINCULADO AL PROYECTO
                insertar_path(path_datos_entrada, global_session.get_id_version(), 'entrada')
                insertar_path(path_datos_salida, global_session.get_id_version(), 'salida')
                #CREO EL PATH DONDE SE VA A EJECUTAR DESARROLLO DEPENDIENDO DEL PROYECYO Y LA VERSION QUE ESTE EN USO
                ##necesito tener el nombre del dataset seleccionado asi le cambio el nombre y lo
                mover = mover_y_renombrar_archivo(global_names_reactivos.get_name_file_db(), global_session.get_path_guardar_dataSet_en_proyectos(), name_suffix, path_datos_entrada)
                
                global_desarollo.script_path = f'./Modelar.sh --input-dir {path_datos_entrada} --output-dir {path_datos_salida}'
                ejectutar_desarrollo_asnyc(click_count_value, mensaje_value, proceso)
                
                
    ##ESTA FUNCION LA HAGO PARA DETECTAR BIEN LOS VALORES REACTIVOS QUE ESTAN DENTRO DEL PROCESO        
    def agregar_reactivo():  
        @reactive.effect
        def insert_data_depends_value():  
            base_datos = "Modeling_App.db"
            if global_desarollo.proceso_ok.get():
                agregar_datos_model_execution(global_session.get_id_version(), global_desarollo.nombre, base_datos , "Exito")
                estado_desarrollo , hora_desarrollo = procesar_etapa(base_datos="Modeling_App.db", id_version=global_session.get_id_version(), etapa_nombre="desarollo")
                global_session_modelos.modelo_desarrollo_estado.set(estado_desarrollo)
                global_session_modelos.modelo_desarrollo_hora.set(hora_desarrollo)
                
            if global_desarollo.proceso_fallo.get():
                agregar_datos_model_execution(global_session.get_id_version(), global_desarollo.nombre, base_datos , "Error")
                estado_desarrollo , hora_desarrollo = procesar_etapa(base_datos="Modeling_App.db", id_version=global_session.get_id_version(), etapa_nombre="desarollo")
                global_session_modelos.modelo_desarrollo_estado.set(estado_desarrollo)
                global_session_modelos.modelo_desarrollo_hora.set(hora_desarrollo)
        
                    
                
    

    agregar_reactivo()        
        
    @output
    @render.text
    def error():
      return mostrar_error(mensaje.get())
               
        

    