from shiny import reactive, render, ui
from funciones.create_param import create_screen
from clases.global_modelo import global_desarollo
from funciones.create_nav_menu import create_nav_menu
from clases.class_screens import ScreenClass
from funciones.utils import retornar_card, mover_files
from clases.class_user_proyectName import global_user_proyecto
from funciones.utils import create_modal_parametros, id_buttons_desa
from clases.global_session import global_session
from funciones.utils_2 import get_user_directory, render_data_summary, aplicar_transformaciones, mostrar_error, cambiarAstring, trans_nulos_adic
from api.db import *
from clases.global_session import *
from clases.reactives_name import global_names_reactivos
from funciones.funciones_cargaDatos import guardar_archivo
from shiny.types import FileInfo
from funciones.help_versios import obtener_opciones_versiones, obtener_ultimo_id_version
from clases.global_session import *
from clases.class_validacion import Validator
from clases.loadJson import LoadJson
from logica_users.var_globales_paths import base_path_entrada, base_path_salida
import os



def server_desarollo(input, output, session, name_suffix):
    directorio_desarollo = reactive.value("")
    screen_instance = reactive.value(None)  # Mantener screen_instance como valor reactivo
    user_id_send = reactive.Value("")
    global_names_reactivos.name_desarrollo_set(name_suffix)
    opciones_data = reactive.Value(None)
    dataSet_predeterminado_parms = reactive.Value(None)
    mensaje = reactive.Value("")
    
    # Diccionario de transformaciones
    transformaciones = {
        'par_ids': cambiarAstring,
        'par_target': cambiarAstring,
        'cols_forzadas_a_predictoras': cambiarAstring,
        'par_var_grupo': cambiarAstring,
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
                    #global_desarollo.script_path = f"./Modelar.sh datos_entrada_{user_id_cleaned} datos_salida_{user_id_cleaned}"
                    
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

    @output
    @render.ui
    def conten_nav():
        return create_nav_menu(name_suffix, name)

    @reactive.Effect
    @reactive.event(input.file_desarollo)
    async def cargar_Datos_desarrollo():
        try:
            file: list[FileInfo] | None = input.file_desarollo()
            input_name = file[0]['name']
            print(input_name)
            global_names_reactivos.set_name_data_Set(input_name)
            ruta_guardado = await guardar_archivo(input.file_desarollo, name_suffix)
            
            global_names_reactivos.set_proceso_leer_dataset(True)
            files_name = get_records(global_session.get_id_proyecto())
            opciones_data.set(obtener_opciones_versiones(files_name, "id_files", "nombre_archivo"))
            dataSet_predeterminado_parms.set(obtener_ultimo_id_version(files_name, "id_files"))
            print(f"El archivo fue guardado en: {ruta_guardado}")
            ui.update_select("files_select", choices=opciones_data.get(), selected=dataSet_predeterminado_parms.get())
            # Después de guardar el archivo, puedes cargar los datos utilizando screen_instance
            #await screen_instance.get().load_data(input.file_desarollo, name_suffix)
            
        except Exception as e:
            print(f"Error en la carga de datos: {e}")

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
            #get_fecha=global_fecha.get_fecha_desarrollo,
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
        proceso = global_desarollo.proceso.get()

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

                json_loader = LoadJson(user_id_cleaned, input) 
                json_loader.inputs.update(inputs_procesados)
                json_file_path = json_loader.loop_json()
                print(f"Inputs guardados en {json_file_path}")
                #CREO EL PATH DONDE SE VA A EJECUTAR DESARROLLO DEPENDIENDO DEL PROYECYO Y LA VERSION QUE ESTE EN USO
                print(global_session.get_id_user(), "ESTOY EN EL USER ID LRPM")
                base_path = base_path_entrada.rstrip(os.sep)
                path_datos_entrada = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_entrada_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}'
                
                path_datos_salida = path_datos_entrada = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}'
                
                
                global_desarollo.script_path = f'./Modelar.sh "{path_datos_entrada}" {path_datos_salida}'
                ejectutar_desarrollo_asnyc(click_count_value, mensaje_value, proceso)

            
        
    @output
    @render.text
    def error():
      return mostrar_error(mensaje.get())
               
        
    
    @reactive.effect
    @reactive.event(input[f'open_html_{global_desarollo.nombre}'])
    def enviar_result():
        ui.update_navs("Resultados_nav", selected="desarrollo")

    def create_modals(id_buttons_desa):
        for id_button in id_buttons_desa:
            @reactive.Effect
            @reactive.event(input[id_button])
            def monitor_clicks(id_button=id_button):
                count.set(count() + 1)	
                if count.get() > 0:
                    print(id_button, count.get())
                    modal = create_modal_parametros(id_button)
                    ui.modal_show(modal)

    create_modals(id_buttons_desa)
