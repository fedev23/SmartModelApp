from shiny import reactive, render, ui
from funciones.create_nav_menu import create_nav_menu
from clases.class_user_proyectName import global_user_proyecto
from clases.class_screens import ScreenClass
from clases.global_name import global_name_manager
from clases.loadJson import LoadJson
from funciones.param_in_sample import param_in_sample
from funciones.utils import transformar_segmentos, validar_columnas, transform_data, transformar_reportes, create_modal_parametros, id_buttons
from global_var import global_data_loader_manager
import pandas as pd
from funciones.utils_2 import cambiarAstring, validar_proyecto, aplicar_transformaciones
from clases.global_session import global_session
from api.db import *
from clases.reactives_name import global_names_reactivos
from api.db import *
from clases.class_validacion import Validator
from clases.global_modelo import modelo_in_sample
from clases.global_modelo import global_desarollo
from funciones.help_versios import copiar_json_si_existe
import os
from funciones.cargar_archivosNEW import mover_y_renombrar_archivo
from funciones.utils import mover_file_reportes_puntoZip

ejemplo_niveles_riesgo = pd.DataFrame({
    "Nombre Nivel": ["BajoBajo", "BajoMedio", "BajoAlto", "MedioBajo", "MedioMedio", "Alto"],
    "Regla": ["> 955", "> 930", "> 895", "> 865", "> 750", "<= 750"],
    "Tasa de Malos Máxima": ["3.0%", "6.0%", "9.0%", "15.0%", "18.0%", "100.0%"]
})

ejemplo_segmentos = pd.DataFrame({
    "Segment": ["Female_Employees", "Male_Employees", "Other", "Other"],
    "Rule": [
        "Gender == 'F' & Job_Type == 'E'",
        "Gender == 'M' & Job_Type == 'E'",
        "Gender == 'F' & (is.na(Job_Type) | Job_Type != 'E')",
        "Gender == 'M' & (is.na(Job_Type) | Job_Type != 'E')"
    ]
})

ejemplos_rangos = pd.DataFrame({
    "Variables de corte": ["Segmento", "TipoOpe, TipoCmr"]
})


styles = {
    "cols": None,  # Aplica a todas las columnas
    "style": {
        "background-color": "gray",  # El color de fondo será gris
        # El texto será blanco (opcional, por visibilidad)
        "color": "white",
        "font-weight": "bold",       # El texto en negrita (opcional)
    }
}


def server_in_sample(input, output, session, name_suffix):
    screen_instance = ScreenClass("", name_suffix)
    mensaje_de_error = reactive.Value("")
    mensaje = reactive.Value("")
    name = "validación in sample"
    data_loader = global_data_loader_manager.get_loader("desarrollo")
    count = reactive.value(0)
    no_error = reactive.Value(True)
    name = "Validacion in sample"
    global_names_reactivos.name_validacion_in_sample_set(name_suffix)



    

    # HAGO EL INPUT FILE DE FILE_DESAROLLO FUNCIONE ACA TAMBIEN, ASI ENVIA EL MISMO ARCHIO A VALIDACION IN SAMPLE

    @output(id=f"summary_data_{name_suffix}")
    @render.data_frame
    def summary_data_desarollo():
        return screen_instance.render_data_summary()

    @output
    @render.ui
    def mostrar_parametros_in_sample():
        return param_in_sample(name_suffix)

    @output
    @render.text
    def nombre_proyecto_in_sample():
        return f'Proyecto: {global_user_proyecto.mostrar_nombre_proyecto_como_titulo(global_session.proyecto_seleccionado())}'
    
    @output
    @render.ui
    def menuInSample():
        return create_nav_menu(name_suffix, name)

    @output
    @render.data_frame
    def par_rango_niveles():
        return render.DataGrid(ejemplo_niveles_riesgo, editable=True, width='500px')
        # ejemplo_niveles_riesgo

    @output
    @render.data_frame
    def par_rango_segmentos():
        return render.DataGrid(ejemplo_segmentos, editable=True,  width='500px')

    @output
    @render.data_frame
    def par_rango_reportes():
        return render.DataGrid(ejemplos_rangos, editable=True,  width='500px')
        # ejemplo_niveles_riesgo
        
        
    transformaciones = {
        'par_vars_segmento': cambiarAstring,
        
    }
    
    ##USO ESTE DECORADOR PARA CORRER EL PROCESO ANSYC Y NO HAYA INTERRUCIONES EN EL CODIGO LEER DOCUENTACION
    #https://shiny.posit.co/py/docs/nonblocking.html
    @ui.bind_task_button(button_id="execute_in_sample")
    @reactive.extended_task
    async def ejecutar_in_sample_ascyn(click_count, mensaje, proceso):
        # Llamamos al método de la clase para ejecutar el proceso
        await modelo_in_sample.ejecutar_proceso_prueba(click_count, mensaje, proceso)
        
    ##Luego utilizo el input del id del boton para llamar ala funcion de arriba y que se ejecute con normalidad
    @reactive.effect
    @reactive.event(input.execute_in_sample, ignore_none=True)
    def ejecutar_in_sample_button():
        click_count_value = global_desarollo.click_counter.get()  # Obtener contador
        mensaje_value = global_desarollo.mensaje.get()  # Obtener mensaje actual
        proceso = global_desarollo.proceso.get()
        validator = Validator(input, global_session.get_data_set_reactivo(), name_suffix)

        # Ejecutar las validaciones
        validator.validate_project()
        validator.validate_columns()
        validator.validate_column_identifiers()
        validator.validate_iv()
        validator.validate_target_column()
        validator.validate_training_split()

        # Verificar si hay errores, ver si agrego una validacion
        if validator.is_valid():
            # Procesar los inputs
            inputs_procesados = {key: transformacion(input[key]()) for key, transformacion in transformaciones.items()}
            rango_reportes = par_rango_reportes.data_view()
            reportesMap = transformar_reportes(rango_reportes)
            segmentos_editados = par_rango_segmentos.data_view()
            segmentosMap = transformar_segmentos(segmentos_editados)
            df_editado = par_rango_niveles.data_view()
            niveles_mapeados = transform_data(df_editado)

            # Guardar los datos procesados
            load_handler = LoadJson(input, global_session.get_id_user().replace('|', '_'))
            load_handler.inputs.update(inputs_procesados)
            load_handler.inputs['par_rango_niveles'] = niveles_mapeados
            load_handler.inputs['par_rango_segmentos'] = segmentosMap
            load_handler.inputs['par_rango_reportes'] = reportesMap
            json_file_path = load_handler.loop_json()
            print(f"Inputs guardados en {json_file_path}")
            
            
            base_path_entrada= '/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_entrada_'
            base_path_salida = '/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_'
            
            destino = os.path.join(base_path_entrada, f'{global_session.get_id_user()}', f'proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}',
                       f'version_{global_session.get_id_version()}_{global_session.get_versiones_name()}',
                       f'version_parametros_{global_session.get_version_parametros_id()}',
                       f'{global_session.get_versiones_parametros_nombre()}')
            
            destino_salida = os.path.join(base_path_salida, f'{global_session.get_id_user()}', f'proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}',
                       f'version_{global_session.get_id_version()}_{global_session.get_versiones_name()}',
                       f'version_parametros_{global_session.get_version_parametros_id()}',
                       f'{global_session.get_versiones_parametros_nombre()}')
            
            
            global_session.set_path_niveles_scorcads(destino)
            global_session.set_path_niveles_scorcads_salida(destino_salida)
            
            copiar_json_si_existe(json_file_path, destino)
            inputs_procesados = aplicar_transformaciones(input, transformaciones)
            insert_table_model(global_session.get_id_user(), global_session.get_id_proyecto(), name_suffix, global_name_manager.get_file_name_desarrollo())
            ##PATH DONDE SE EJECUTA EL SCRIPT Y LAS CARPETAS QUE CORRESPONDEN AL USARIO, PROYECT, VERSION ACTUAL O EN
            mover_y_renombrar_archivo(global_names_reactivos.get_name_file_db(), global_session.get_path_guardar_dataSet_en_proyectos(), name_suffix, base_path_entrada)
            modelo_in_sample.script_path = f"./Validar_Desa.sh {global_session.get_path_niveles_scorcads()} {global_session.get_path_niveles_scorcads_salida}"
            ejecutar_in_sample_ascyn(click_count_value, mensaje_value, proceso) #-->EJECUTO EL PROCESO ACA
     
        else:
            # Mostrar errores
            mensaje_de_error.set("\n".join(validator.get_errors()))
            no_error.set(False)
            mensaje.set("")
        
    
    @output
    @render.ui
    def salida_error():
        if mensaje_de_error.get():
            ui.notification_show(
                ui.p(f"Error:", style="color: red;"),
                action=ui.p(mensaje_de_error.get(),
                            style="font-style: italic;"),
                duration=7,
                close_button=True
            )

    # Función para crear los monitores de clics para cada botón
    # print(id_buttons)

    def create_modals(id_buttons):
        id_buttons.extend(["help_niveles", "help_rangos", "help_segmentos"])
        for id_button in id_buttons:
            # Crear un efecto reactivo para cada botón en la lista
            @reactive.Effect
            @reactive.event(input[id_button])
            # id_button se pasa como argumento con valor predeterminado
            def monitor_clicks(id_button=id_button):
                count.set(count() + 1)
                if count.get() > 1:
                    modal = create_modal_parametros(id_button)
                    ui.modal_show(modal)

    # Llamar a la función con la lista de botones
    create_modals(id_buttons)
