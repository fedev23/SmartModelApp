from shiny import reactive, render, ui
from clases.class_user_proyectName import global_user_proyecto
from clases.class_screens import ScreenClass
from datetime import datetime
from clases.loadJson import LoadJson
from funciones.param_in_sample import param_in_sample
from funciones.utils import transformar_segmentos, transform_data, transformar_reportes, create_modal_parametros, id_buttons
import pandas as pd
from funciones.utils import mover_file_reportes_puntoZip
from funciones.utils_2 import cambiarAstring, aplicar_transformaciones
from clases.global_session import global_session
from api.db import *
from clases.reactives_name import global_names_reactivos
from api.db import *
from clases.class_validacion import Validator
from clases.global_modelo import modelo_in_sample
from clases.global_modelo import global_desarollo
import os
from funciones.cargar_archivosNEW import mover_y_renombrar_archivo
from funciones.utils_cargar_json import update_dataframe_from_json, actualizar_json
from clases.global_sessionV2 import *
from clases.global_reactives import *
from api.db.sqlite_utils import *
from servers.utils import help_params

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
    "Variables de corte": ["Variable1", "Variable_otro_Seg, Variable_otro_Seg2"]
})



def server_in_sample(input, output, session, name_suffix):
    screen_instance = ScreenClass("", name_suffix)
    mensaje_de_error = reactive.Value("")
    mensaje = reactive.Value("")
    count = reactive.value(0)
    no_error = reactive.Value(True)
    global_names_reactivos.name_validacion_in_sample_set(name_suffix)
    # Inicializamos el estado reactivo del dataset
    data_set = reactive.Value(pd.DataFrame({"Variables de corte": []}))
    list_transformada = reactive.Value([])


    

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
    
    
    @reactive.Effect
    @reactive.event(input.add_fila)
    def evento_agregar_nueva_fila():
        print("pase??")
        data = par_rango_reportes.data_view()
        new_row = pd.DataFrame({"Variables de corte": ["Insertar Valores"]})
        data = pd.concat([data, new_row], ignore_index=True)
        data_set.set(data)
        print(data)

   
  
    @output
    @render.data_frame
    def par_rango_niveles():
        # Obtén el diccionario con los DataFrames
        if global_session_V2.get_json_params_desarrollo() is not None:
            df_dict = update_dataframe_from_json(global_session_V2.get_json_params_desarrollo())
            
            # Asegúrate de que 'niveles_riesgo' esté en el diccionario y sea un DataFrame válido
            if "par_rango_niveles" in df_dict and isinstance(df_dict["par_rango_niveles"], pd.DataFrame):
                df_niveles_riesgo = df_dict["par_rango_niveles"]
                return render.DataGrid(df_niveles_riesgo, editable=True, width='500px')
                #print(df_niveles_riesgo, "que tiene este df?")
            else:
                print("Error: 'niveles_riesgo' no es un DataFrame válido o está ausente.")
                return render.DataGrid(ejemplo_niveles_riesgo, editable=True, width='500px')

            # Renderizar el DataFrame específico
            #return render.DataGrid(df_niveles_riesgo, editable=True, width='500px')
            
    @output
    @render.data_frame
    def par_rango_segmentos():
        if global_session_V2.get_json_params_desarrollo() is not None:
            df_dict = update_dataframe_from_json(global_session_V2.get_json_params_desarrollo())
            
            if "par_rango_segmentos" in df_dict and isinstance(df_dict["par_rango_segmentos"], pd.DataFrame):
                df_niveles_segmentos = df_dict["par_rango_segmentos"]
                print(df_niveles_segmentos)
                return render.DataGrid(df_niveles_segmentos, editable=True,  width='500px')
                #print(df_niveles_riesgo, "que tiene este df?")
            else:
                print("Error: 'niveles_riesgo' no es un DataFrame válido o está ausente.")
                #return render.DataGrid(ejemplo_niveles_riesgo, editable=True, width='500px')


    @output
    @render.data_frame
    def par_rango_reportes():
        # Obtén los datos del estado reactivo
        data = data_set.get()
        
        # Si el DataFrame está vacío, usa el DataFrame de ejemplo
        if data.empty:
            return render.DataGrid(ejemplos_rangos, editable=True, width="500px")
        
        # De lo contrario, renderiza los datos actuales
        return render.DataGrid(data, editable=True, width="500px")
   
        
    transformaciones = {
        'par_vars_segmento': cambiarAstring,
        
    }
    
    @reactive.effect
    @reactive.event(input.par_vars_segmento)
    def ver_input():
        print("hola??")
        print(f"{input.par_vars_segmento()} estoy haciendo elprint??")
        valor1 = input.par_vars_segmento()
        trans_formara_lista = list(valor1)
        list_transformada.set(trans_formara_lista)
        #print(trans_formara_lista)
        

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
        # Verificar si hay errores, ver si agrego una validacion
        if validator.is_valid():
            # Procesar los inputs
            inputs_procesados = {key: transformacion(input[key]()) for key, transformacion in transformaciones.items()}
            #par_rango_reportes.data_view()
            rango_reportes = par_rango_reportes.data_view()
            reportesMap = transformar_reportes(rango_reportes)
            #segmentos_editados = par_rango_segmentos.data_view()
            #segmentosMap = transformar_segmentos(segmentos_editados)
            df_editado = par_rango_niveles.data_view()
            niveles_mapeados = transform_data(df_editado)
            # Guardar los datos procesados
            json_loader = LoadJson(input)

# Imprimir los inputs cargados
            print("Inputs cargados:", json_loader.inputs)
            json_loader.inputs['delimiter_desarollo'] = global_estados.get_delimitador()
            json_loader.inputs['proyecto_nombre'] = global_session.get_name_proyecto()
                
            json_loader.inputs['par_rango_niveles'] = niveles_mapeados
            #load_handler.inputs['par_rango_segmentos'] = segmentosMap
            json_loader.inputs['par_rango_reportes'] = reportesMap
            #json_file_path = json_loader.load_json()
            nuevos_valores = {
                "delimiter_desarollo": global_estados.get_delimitador(),
                "proyecto_nombre": global_session.get_name_proyecto(),
                "par_rango_niveles": niveles_mapeados,
                "par_rango_reportes": reportesMap,
            }

            # Actualizar el JSON con los nuevos valores
            json_loader.update_values(nuevos_valores)
            json_loader.save_json()
            
            path_entrada = obtener_path_por_proyecto_version(global_session.get_id_version(), 'entrada')
            path_salida = obtener_path_por_proyecto_version(global_session.get_id_version(), 'salida')

            #path = obtener_path_por_id_json("Modeling_App.db", global_session.get_version_parametros_id())
            path_datos_entrada = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_entrada_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}/version_parametros_{global_session.get_version_parametros_id()}_{global_session.get_versiones_parametros_nombre()}'
            global_session.get_version_parametros_id()
            #C:\Users\fvillanueva\Desktop\SmartModel_new_version\new_version_new\Automat\datos_entrada_auth0_670fc1b2ead82aaae5c1e9ba\proyecto_57_Proyecto_prueba_De_Datos\version_59_c\version_parametros_42_version_c
            #path_si_existe_version = path_entrada.join()
            global_session.set_path_niveles_scorcads(path_datos_entrada)
            global_session.set_path_niveles_scorcads_salida(path_salida)
            
            ##COPIO EL JSON DE LA CARPETA y lo fusion por si hay IN SAMPLE
            #json = copiar_json_si_existe(path_entrada, path_datos_entrada)

            inputs_procesados = aplicar_transformaciones(input, transformaciones)
            
            origen_modelo_puntoZip =  f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}'
            ##MUEVO EL MODELO .ZIP QUE GENERO DESARROLO PARA QUE PUEDA SER USADO, ESTO DEBERIA SER USANDO EN TODAS LAS ISTANCIAS DE LOS MODELOS
            movi = mover_file_reportes_puntoZip(origen_modelo_puntoZip,path_datos_entrada )
            print (f"movi .zip a {movi}")
            
            #insert_table_model(global_session.get_id_user(), global_session.get_id_proyecto(), name_suffix, global_name_manager.get_file_name_desarrollo())
            ##PATH DONDE SE EJECUTA EL SCRIPT Y LAS CARPETAS QUE CORRESPONDEN AL USARIO, PROYECT, VERSION ACTUAL O EN
            mover_y_renombrar_archivo(global_names_reactivos.get_name_file_db(), global_session.get_path_guardar_dataSet_en_proyectos(), name_suffix, path_entrada)
            
            modelo_in_sample.script_path = f"./Validar_Desa.sh  --input-dir {global_session.get_path_niveles_scorcads()} --output-dir {global_session.get_path_niveles_scorcads_salida()}"
            
            ejecutar_in_sample_ascyn(click_count_value, mensaje_value, proceso) #-->EJECUTO EL PROCESO ACA
            if modelo_in_sample.proceso.get():
                    estado = insert_table_model(global_session.get_id_user(), global_session.get_id_proyecto(), datetime.now().strftime("%Y-%m-%d %H:%M"), modelo_in_sample.nombre, global_names_reactivos.get_name_file_db(), global_session.get_id_version(), 'in_sample', 'completado')
                    print(f'estado de la ejecucion {estado}')
            else:
                    estado = insert_table_model(global_session.get_id_user(), global_session.get_id_proyecto(), datetime.now().strftime("%Y-%m-%d %H:%M"), modelo_in_sample.nombre, global_names_reactivos.get_name_file_db(), global_session.get_id_version(), 'in_sample', 'error')
                    print(f'estado de la ejecucion {estado}')
                 
     
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
