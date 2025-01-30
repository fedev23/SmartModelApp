from shiny import reactive, render, ui
from funciones.create_param import create_screen
from clases.global_modelo import global_desarollo
from clases.class_screens import ScreenClass
from funciones.utils import retornar_card
from funciones_modelo.warning_model import *
from funciones.utils_2 import *
from api.db import *
from clases.global_session import *
from clases.global_sessionV2 import *
from clases.reactives_name import global_names_reactivos
from clases.global_session import *
from clases.class_validacion import Validator
from clases.loadJson import LoadJson
from clases.global_reactives import global_estados
from funciones.cargar_archivosNEW import mover_y_renombrar_archivo
from funciones.clase_estitca.cargar_files import FilesLoad
from clases.reactives_name import global_names_reactivos
from global_names import global_name_desarrollo
from funciones_modelo.global_estados_model import global_session_modelos
from api.db.sqlite_utils import *
from funciones_modelo.global_estados_model import global_session_modelos
from funciones_modelo.global_estados_model import global_session_modelos
from funciones_modelo.help_models import *
import asyncio, time


def server_desarollo(input, output, session, name_suffix):
    clase_cargar_files = FilesLoad(name_suffix)
    click = reactive.value(0)
    directorio_desarollo = reactive.value("")
    screen_instance = reactive.value(None)  # Mantener screen_instance como valor reactivo
    user_id_send = reactive.Value("")
    global_names_reactivos.name_desarrollo_set(name_suffix)
    mensaje = reactive.Value("")
    file_lines = reactive.value()
    termino = reactive.value(False)
    primer_file = reactive.Value(True)
    segundo_file = reactive.Value(False)
    
    
    # Diccionario de transformaciones
    transformaciones = {
        'par_ids': cambiarAstring,
        #'par_target': cambiarAstring,
        'par_vars_segmento': to_empty_list,
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

    
    @reactive.Effect
    @reactive.event(input.file_desarollo)
    async def datos_desarrolo():
        await clase_cargar_files.cargar_Datos_desarrollo(input.file_desarollo)
    
    @reactive.Effect
    @reactive.event(input.cancel_overwrite)
    def overwrite_file():
        return  ui.modal_remove()
            
    
    @reactive.Effect
    @reactive.event(input.cancel_overwrite_desarollo)
    def overwrite_file():
        #global_session_V2.boolean_for_change_file.set(False)
        global_session_V2.count_global.set(1) 
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
        file_name = global_names_reactivos.get_name_file_db()
        hora = global_session_modelos.modelo_desarrollo_hora.get()
        estado = global_session_modelos.modelo_desarrollo_estado.get()
        mensaje_error = global_session_modelos.modelo_desarrollo_mensaje_error.get()
        
        print(mensaje_error, "mensaje error en desa")
        # Llamar a retornar_card con valores validados
        return retornar_card(
            get_file_name=file_name,
            modelo=global_desarollo,
            fecha=hora,
            estado=estado,
            mensaje_error=mensaje_error
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
        porcentaje = global_desarollo.porcentaje.get()
        base_datos = 'Modeling_App.db'
        
        validar_si_existe_version = check_if_exist_id_version(global_session.get_id_version())
        if validar_si_existe_version:
            ui.modal_show(create_modal_generic("boton_advertencia_ejecute_desa", f"Es obligatorio generar una versión para continuar en {global_name_desarrollo}."))
            return
        
        validacion_existencia_modelo =  verificar_estado_modelo(base_datos, version_id=global_session.get_id_version(), dataset_id=global_session.get_id_dataSet())
        
        if validacion_existencia_modelo:
            return ui.modal_show(create_modal_generic("close_button_modelo_ok", f"Ya existe un modelo generado para la version {global_session.get_versiones_name()}"))
          
        
        # Crear instancia de la clase Validator
        if global_desarollo.pisar_el_modelo_actual.get() or validacion_existencia_modelo:
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
                    #CREO EL PATH DONDE SE VA A EJECUTAR DESARROLLO DEPENDIENDO DEL PROYECYO Y LA VERSION QUE ESTE EN USO

                    ##NECESITO NOMBRE DEL PROYECTO Y NOMBRE DE LA VERSION NO ORIGINAL, SINO MAS BIEN CON ESPACIOS
                    
                    path_datos_entrada = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_entrada_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}'
                    path_datos_salida  = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}'
                    
                    global_desarollo.porcentaje_path = path_datos_salida
                    ##necesito tener el nombre del dataset seleccionado asi le cambio el nombre y lo
                    data_Set  = get_datasets_directory(global_session.get_id_user(), global_session.get_id_proyecto(), global_session.get_name_proyecto())
        
                    mover_y_renombrar_archivo(global_names_reactivos.get_name_file_db(), data_Set, name_suffix, path_datos_entrada)
                    
                    print("hasta aca llego? ")
                    global_desarollo.script_path = f'./Modelar.sh --input-dir {path_datos_entrada} --output-dir {path_datos_salida}'
                    ejectutar_desarrollo_asnyc(click_count_value, mensaje_value, proceso)
                    click.set(click() + 1)
                    global_desarollo.pisar_el_modelo_actual.set(False)
                    
                    
                
    ##ESTA FUNCION LA HAGO PARA DETECTAR BIEN LOS VALORES REACTIVOS QUE ESTAN DENTRO DEL PROCESO        
    def agregar_reactivo():  
        @reactive.effect
        def insert_data_depends_value():  
            base_datos = "Modeling_App.db"
            if global_desarollo.proceso_ok.get():
                agregar_datos_model_execution(global_session.get_id_version(), global_desarollo.nombre, global_names_reactivos.get_name_file_db(), "Exito", dataset_id=global_session.get_id_dataSet())
                estado_desarrollo , hora_desarrollo, mensaje_error = procesar_etapa(base_datos="Modeling_App.db", id_version=global_session.get_id_version(), etapa_nombre="desarollo")
                global_session_modelos.modelo_desarrollo_estado.set(estado_desarrollo)
                global_session_modelos.modelo_desarrollo_hora.set(hora_desarrollo)
                global_desarollo.proceso_ok.set(False)
                
            if global_desarollo.proceso_fallo.get():
                agregar_datos_model_execution(global_session.get_id_version(), global_desarollo.nombre, global_names_reactivos.get_name_file_db(), "Error", mensaje_error=global_desarollo.mensaje.get(), dataset_id=global_session.get_id_dataSet())
                estado_desarrollo , hora_desarrollo, mensaje_error = procesar_etapa(base_datos="Modeling_App.db", id_version=global_session.get_id_version(), etapa_nombre="desarollo")
                global_session_modelos.modelo_desarrollo_estado.set(estado_desarrollo)
                global_session_modelos.modelo_desarrollo_mensaje_error.set(mensaje_error)
                global_session_modelos.modelo_desarrollo_hora.set(hora_desarrollo)
                global_desarollo.proceso_fallo.set(False)
        
                    
    agregar_reactivo()        
        
    @output
    @render.text
    def error():
      return mostrar_error(mensaje.get())
  
  
  
    @reactive.Effect
    @reactive.event(input["continuar_no_overwrite_desarollo"])
    def valid_model_of_sample():
        global_desarollo.pisar_el_modelo_actual.set(True)
        return  ui.modal_remove()
               
        
    
    @reactive.Effect
    @reactive.event(input["cancel_overwrite_desarrollo"])
    def cancelar():
        return ui.modal_remove()
  
    
    @reactive.effect
    @reactive.event(input.boton_advertencia_ejecute_desa)
    def ok_no():
        return ui.modal_remove()
    
    
            
        
    @reactive.calc
    def leer_archivo():
        """Lee el archivo de progreso y actualiza la UI."""
        if termino.get() is False:
            
            if click.get() < 1:
                return ""

            if global_desarollo.proceso_fallo.get():
                return

            path = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}'
            name_file = "progreso.txt"

            # Obtener el último porcentaje del archivo
            ultimo_porcentaje = monitorizar_archivo(path, nombre_archivo=name_file)
            file_lines.set(ultimo_porcentaje)
                
            if primer_file.get():
                if ultimo_porcentaje == "100%":
                    file_lines.set("100%")
                    primer_file.set(False)
                    
            if file_lines.get() != "100%" and primer_file.get() is False:
                segundo_file.set(True)  
          
            print("esperando pasar...")
            if segundo_file.get():
                print("pase...")
                file_lines.set(f"Procesando segunda etapa.. {ultimo_porcentaje}")
                if ultimo_porcentaje == "100%":
                    print("cuando paso a esta validacion?")
                    global_desarollo.eliminar_archivo_progreso(path, name_file)
                    return "100%"
                

            # Actualizar variable reactiva
            print(f"Último porcentaje capturado: {file_lines.get()}")

            # Reactivar cada 3 segundos si aún no ha llegado al 100% o si sigue habiendo actividad
            reactive.invalidate_later(2)

            return file_lines.get()

    # Mostrar el contenido del archivo en la UI
    @render.ui
    def value_desarollo():
        if click.get() >= 1:
            return f"Porcentaje: {leer_archivo()}"
   
    
    @reactive.effect
    @reactive.event(input.close_button_modelo_ok)
    def close_modal():
        return ui.modal_remove()

   
    