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
from funciones.utils_2 import cambiarAstring, validar_proyecto
from clases.global_session import global_session
from api.db import *
from clases.reactives_name import global_names_reactivos


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
    name = "validación in sample"
    data_loader = global_data_loader_manager.get_loader("desarrollo")
    count = reactive.value(0)
    no_error = reactive.Value(True)
    name = "Validacion in sample"
    global_names_reactivos.name_validacion_in_sample_set(name_suffix)

    def create_navigation_handler_validacion(input_id, screen_name, valid):
        @reactive.Effect
        @reactive.event(input[input_id])
        async def navigate():
            if valid.get():
                await session.send_custom_message('navigate', screen_name)

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
    @reactive.Effect
    @reactive.event(input[f'load_param_{name_suffix}'])
    def validacion():
        error_messages = []

        # 1. Validar si el dataset está cargado
        if not global_name_manager.name_file_desarrollo.get():
            error_messages.append(f"No se ha ingresado ningún dataset en {name}")
            mensaje_de_error.set("\n".join(error_messages))
            no_error.set(False)
            return  # Detener la ejecución si no hay dataset

        # 2. Obtener el dataset
        df = data_loader.getDataset()
        inputs_procesados = {key: transformacion(input[key]()) for key, transformacion in transformaciones.items()}

        # 3. Validar si el proyecto está asignado
        proyecto_nombre = global_session.get_id_user()
        if not validar_proyecto(proyecto_nombre):
            error_messages.append(f"Es necesario tener un proyecto asignado o creado para continuar en {name}")
            mensaje_de_error.set("\n".join(error_messages))
            no_error.set(False)
            return  # Detener la ejecución si no hay proyecto asignado

        # 4. Validar las columnas
        par_vars_segmento = input['par_vars_segmento']()
        columnas_validas = validar_columnas(df, par_vars_segmento)
        
        if not columnas_validas:
            error_messages.append(f"Error en columnas: {par_vars_segmento}, no encontradas en el dataset.")
        
        # 5. Procesar los demás inputs solo si no hubo errores previos
        if not error_messages:
            rango_reportes = par_rango_reportes.data_view()
            reportesMap = transformar_reportes(rango_reportes)

            segmentos_editados = par_rango_segmentos.data_view()
            segmentosMap = transformar_segmentos(segmentos_editados)

            df_editado = par_rango_niveles.data_view()
            niveles_mapeados = transform_data(df_editado)
            ##global session es el manejo de los usarios.
            if global_session.proceso.get():
                state = global_session.session_state.get()
                if state["is_logged_in"]:
                    user_id = state["id"]
                    user_id_cleaned = user_id.replace('|', '_')
            # Guardar los datos procesados en un archivo JSON
                    load_handler = LoadJson(input, user_id_cleaned)
                    load_handler.inputs['par_rango_niveles'] = niveles_mapeados
                    load_handler.inputs['par_rango_segmentos'] = segmentosMap
                    load_handler.inputs['par_rango_reportes'] = reportesMap
                    load_handler.inputs['par_vars_segmento'] = par_vars_segmento
                    load_handler.inputs.update(inputs_procesados)

                    json_file_path = load_handler.loop_json()
                    print(f"Inputs guardados en {json_file_path}, en {name_suffix}")
                    create_navigation_handler_validacion(f'load_param_{name_suffix}', 'Screen_3', no_error)
                    ui.update_accordion("my_accordion", show=["in_sample"])
        else:
            # Mostrar mensajes de error si existen
            mensaje_de_error.set("\n".join(error_messages))
            no_error.set(False)
        
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

    def create_navigation_handler(input_id, screen_name):
        @reactive.Effect
        @reactive.event(input[input_id])
        async def navigate():
            await session.send_custom_message('navigate', screen_name)
    # Navegaciones, hago siempre la misma funcion por un tema de simplicidad por el momento, ya que a el ser efectos reactivos crearla en utils, puede ser un trabajo que no haria falta por 3 lineas de codigo

    create_navigation_handler('start_in_sample', 'Screen_User')
    create_navigation_handler('screen_in_sample', 'screen_in_sample')
    create_navigation_handler('screen_Desarollo_in_sample', 'Screen_Desarollo')
    create_navigation_handler('load_in_sample', 'Screen_valid')
    create_navigation_handler('load_Validacion_in_sample', 'Screen_Porduccion')
    create_navigation_handler(f"ir_modelos_{name_suffix}", "Screen_3")
    create_navigation_handler("ir_result_in_sample", "Screen_Resultados")
    create_navigation_handler("volver_inSample", "Screen_User")
