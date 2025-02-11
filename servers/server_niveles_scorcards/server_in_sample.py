from shiny import reactive, render, ui
from clases.class_screens import ScreenClass
from clases.loadJson import LoadJson
from funciones.param_in_sample import param_in_sample
from funciones.utils import transform_data, transformar_reportes, create_modal_parametros, id_buttons
import pandas as pd
from funciones.utils import mover_file_reportes_puntoZip, retornar_card, eliminar_filas_seleccionadas
from funciones.utils_2 import cambiarAstring, aplicar_transformaciones, get_datasets_directory
from clases.global_session import global_session
from api.db import *
from clases.reactives_name import global_names_reactivos
from api.db import *
from api.db.help_config_db import *
from clases.class_validacion import Validator
from clases.global_modelo import modelo_in_sample
from clases.global_modelo import global_desarollo
from funciones.help_parametros.valid_columns import *
from funciones.cargar_archivosNEW import mover_y_renombrar_archivo
from funciones.utils_cargar_json import update_dataframe_from_json
from clases.global_sessionV2 import *
from clases.global_reactives import *
from api.db.sqlite_utils import *
from funciones_modelo.warning_model import *
from funciones_modelo.global_estados_model import global_session_modelos
from funciones_modelo.help_models import *
from global_names import global_name_in_Sample
from funciones.utils_cargar_json import *
from clases.global_sessionV3 import *

ejemplo_niveles_riesgo = pd.DataFrame({})


ejemplo_niveles_riesgo_2 = pd.DataFrame({
    "Nombre Nivel": ["BajoBajo", "BajoMedio", "BajoAlto", "MedioBajo", "MedioMedio", "Alto"],
    "Regla": [" > 955", "> 930", "> 895", "> 865", "> 750", "<= 750"],
    "Tasa de Malos Máxima": ["3.0%", "6.0%", "9.0%", "15.0%", "18.0%", "100.0%"]
})

##HACER QUE ORDENE POR ORDEN ALFABETICA

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
    "Variables de corte": []
})



def server_in_sample(input, output, session, name_suffix):
    screen_instance = ScreenClass("", name_suffix)
    mensaje_de_error = reactive.Value("")
    inserto = reactive.Value(False)
    mensaje = reactive.Value("")
    count = reactive.value(0)
    count_add_files = reactive.Value(0)
    no_error = reactive.Value(True)
    fila_insert = reactive.Value(False)
    global_names_reactivos.name_validacion_in_sample_set(name_suffix)
    data_set = reactive.Value(pd.DataFrame({"Variables de corte": []}))
    values_tabla_niveles = reactive.Value(pd.DataFrame({"Nombre Nivel": [], "Regla": [], "Tasa de Malos Máxima": []}))
    list_transformada = reactive.Value([])
    click = reactive.Value(0)
    alamacen_data_json = reactive.Value()
   
    



    
    def create_navigation_handler(input_id, screen_name):
        @reactive.Effect
        @reactive.event(input[input_id])
        async def navigate():
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

    
    
    @reactive.Effect
    @reactive.event(input.add_fila)
    def evento_agregar_nueva_fila():
        count_add_files.set(count() + 1)
        column_names = get_categorical_columns_with_unique_values_range(global_session.get_data_set_reactivo(), min_unique=global_session.value_min_for_seg.get(), max_unique=global_session.value_max_for_seg.get())
        #column_names = df.columns.tolist()
        ui.update_selectize("agregar_filas", choices=column_names)
       
        
    @reactive.Effect
    @reactive.event(input.save_modal)
    def valor_min_and_max_ingresado_para_seg():
        min = input.min_value()
        global_session.value_min_for_seg.set(min)
        max = input.max_value()
        global_session.value_max_for_seg.set(max)
        dark_or_light = input.dark_mode_switch()
        
        insertar_configuracion_usuario_con_replace(
            db_path="Modeling_App.db",
            hash_user_id= global_session.get_id_user(),
            valor_min_seg=global_session.value_min_for_seg.get(),
            valor_max_seg=global_session.value_max_for_seg.get(),
            num_select_filas= global_estados.get_numero_dataset(),
            #value_dark_or_light=dark_or_light
        )
        
        count_add_files.set(0)
        create_navigation_handler("save_modal","Screen_User")
        
        #return ui.modal_remove()
        
    
                                               
    
    
    @reactive.effect
    @reactive.event(input.add_files_niveles_riesgo_2)
    def agregar_nombre_nivel():
        nombre_seleccionado = input.add_value().strip()  # Eliminar espacios en blanco

        
        data = values_tabla_niveles.get()   
        # Buscar si hay una fila existente sin valores en "Regla" o "Tasa de Malos Máxima"
        index_vacio = data.index[(data["Regla"] == "") & (data["Tasa de Malos Máxima"] == "")].min()

        if pd.notna(index_vacio):  # Si hay una fila vacía, llenarla con el nombre en lugar de crear una nueva
            data.at[index_vacio, "Nombre Nivel"] = nombre_seleccionado
        else:
            # Determinar el número incremental
            numero_incremental = len(data) + 1
            numero_formateado = f"{numero_incremental:02}"

            # Crear el nombre de nivel con su número incremental
            nuevo_nombre = f"{numero_formateado}_{nombre_seleccionado}"

            # Agregar la nueva fila con el nombre y dejar "Regla" y "Tasa de Malos Máxima" vacíos
            new_row = pd.DataFrame({"Nombre Nivel": [nuevo_nombre], "Regla": [""], "Tasa de Malos Máxima": [""]})
            data = pd.concat([data, new_row], ignore_index=True)  # Agregar la nueva fila al final

        # Actualizar la tabla reactiva
        inserto.set(True)
        values_tabla_niveles.set(data)


    @reactive.effect
    @reactive.event(input.add_files_niveles_riesgo_2)
    def agregar_regla():
        regla = input.add_regla().strip()

        # Si la regla está vacía, asignar un valor por defecto (en este caso, una cadena vacía)
        if not regla:
            regla = ""

        # Obtener el DataFrame actual de la tabla
        data = values_tabla_niveles.get()

        # Buscar la primera fila con un "Nombre Nivel" pero sin "Regla"
        index_vacio = data.index[(data["Regla"] == "") & (data["Nombre Nivel"] != "")].min()

        if pd.notna(index_vacio):  # Si hay una fila vacía, llenar con la regla
            data.at[index_vacio, "Regla"] = regla
        

        # Actualizar la tabla reactiva
        values_tabla_niveles.set(data)


    @reactive.effect
    @reactive.event(input.add_files_niveles_riesgo_2)
    def agregar_Tasa_malos():
        tasa_malos = input.add_tasa_malos().strip()
        
        if not tasa_malos:
            tasa_malos = ""
        else:
            tasa_malos = float(tasa_malos)  # Convertir a float
            tasa_malos = f"{tasa_malos}%" 
            #tasa_malos = f"{tasa_malos}%"  # Agregar el símbolo '%' al final

      
        # Obtener el DataFrame actual de la tabla
        data = values_tabla_niveles.get()

        # Buscar la primera fila con un "Nombre Nivel" pero sin "Tasa de Malos Máxima"
        index_vacio = data.index[(data["Tasa de Malos Máxima"] == "") & (data["Nombre Nivel"] != "")].min()

        if pd.notna(index_vacio):  # Si hay una fila vacía, llenar
            data.at[index_vacio, "Tasa de Malos Máxima"] = tasa_malos
        

        # Actualizar la tabla reactiva con la nueva tasa incluida
        values_tabla_niveles.set(data)
    
    @reactive.effect
    @reactive.event(input.eliminar_filas_par_rango_niveles)
    def eliminar_filas():
        data = values_tabla_niveles.get()  # Obtener el DataFrame actual
        filas = par_rango_niveles.cell_selection()["rows"]  # Obtener filas seleccionadas

        if filas:
            data_editado = eliminar_filas_seleccionadas(data, filas)
            values_tabla_niveles.set(data_editado)  # Actualizar el dataset reactivo con las filas eliminadas
        else:
            print("No hay filas seleccionadas para eliminar.")
            
    @reactive.effect
    def actualizar_insertados():
        if inserto.get():
            
            # Actualizar los valores de los inputs usando `session.send_input_message`
            session.send_input_message("add_value", {"value": ""})
            session.send_input_message("add_regla", {"value": ""})
            session.send_input_message("add_tasa_malos", {"value": ""})
            
            inserto.set(False)  # Resetear la variable reactiva
        

       
 
    
    
    @output
    @render.ui
    def selector():
        if count_add_files.get() >= 1:
            return  ui.input_selectize("agregar_filas","Insertar valores",choices=[],  # Initially empty; will be updated reactively
                                     multiple=True,
                                     options={
                                    "placeholder": "seleccionar columnas..."}
                                 )
        count_add_files.set(0)
        
    
    @reactive.Effect
    @reactive.event(input.add_fila)
    def evento_agregar_nueva_fila():
        count_add_files.set(count() + 1)
        column_names = get_categorical_columns_with_unique_values_range(global_session.get_data_set_reactivo(), min_unique=global_session.value_min_for_seg.get(), max_unique=global_session.value_max_for_seg.get())
        #column_names = df.columns.tolist()
        ui.update_selectize("agregar_filas", choices=column_names)
    
   
        
    @output
    @render.ui
    def insert():
      if count_add_files.get() >= 1:
            return ui.input_action_link("insert_Values", "Insertar")
          
    @reactive.Effect
    @reactive.event(input.insert_Values)
    def insertar_values():
        valores_seleccionados = input.agregar_filas()
        
        if valores_seleccionados:
            # Obtener el DataFrame actual
            fila_insert.set(True)
            valores_seleccionados = cambiarAstring(valores_seleccionados)
            data = par_rango_reportes.data_view()

            # Validar si los valores ya existen
            if valores_seleccionados in data["Variables de corte"].values:
                return  # Salir sin realizar cambios

            # Crear una nueva fila con los valores seleccionados
            new_row = pd.DataFrame({
                "Variables de corte": [valores_seleccionados]  # Se almacenan como array o lista
            })
            
            # Combinar el DataFrame existente con la nueva fila
            data = pd.concat([data, new_row], ignore_index=True)
            
            # Actualizar el DataFrame reactivo
            data_set.set(data)
            count_add_files.set(0)
        else:
            print("No se seleccionaron valores. Operación abortada.")



    @output
    @render.ui
    def delete():
      if fila_insert.get():
            return ui.input_action_link("delete_values", "Eliminar la  fila seleccionada")
        
    
    
    @reactive.Effect
    @reactive.event(input.delete_values)
    def delete_values(): 
        data = data_set.get()
        rows = par_rango_reportes.cell_selection()["rows"]
        
        if rows:  # Verifica si hay filas seleccionadas
            # Asegurarse de que `rows` sea una lista de índices enteros
            selected_rows = sorted([int(row) for row in rows])
            
            print(f"Índices seleccionados para eliminar: {selected_rows}")
            
            # Eliminar las filas seleccionadas del DataFrame
            try:
                updated_data = data.drop(index=selected_rows).reset_index(drop=True)
                
                # Actualizar el dataset reactivo con las filas eliminadas
                data_set.set(updated_data)
                print("Filas eliminadas exitosamente.")
            except KeyError as e:
                print(f"Error al intentar eliminar filas: {e}")
        else:
            print("No se seleccionaron filas para eliminar.")
    
        
    
   
    
    @output
    @render.data_frame
    def par_rango_niveles():
        data = values_tabla_niveles.get()
        json_params = global_session_V3.json_params_insa.get()

        df_niveles = get_parameter_dataframe("par_rango_niveles", json_params)
        if df_niveles is not None and not df_niveles.empty:
            alamacen_data_json.set(df_niveles)
            data = alamacen_data_json.get()
            return render.DataGrid(data, selection_mode="rows",  width="700px")
        
            
        ejemplo_niveles_riesgo_2 = pd.DataFrame({
        "Nombre Nivel": [],
        "Regla": [],
        "Tasa de Malos Máxima": []
    })
        if data is not None and not data.empty:
            
         
            return render.DataGrid(data, selection_mode="rows",  width="700px")
        
        return render.DataGrid(ejemplo_niveles_riesgo_2, selection_mode="rows",  width="700px")
    
    
    
    
    
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
        json_params = global_session_V3.json_params_insa.get()

        df_rango_repotes = get_parameter_dataframe("par_rango_reportes", json_params)
        
        if df_rango_repotes is not None and not df_rango_repotes.empty:
            data = df_rango_repotes
            return render.DataGrid(data, selection_mode="rows",  width="500px")
        
            
        ejemplos_rangos = pd.DataFrame({
            "Variables de corte": []
        })
        
        # Si el DataFrame está vacío, usa el DataFrame de ejemplo
        if data is not None and not data.empty:
            return render.DataGrid(data, selection_mode="rows",  width="500px")
        
        return render.DataGrid(ejemplos_rangos, selection_mode="rows",  width="500px")
        
        # De lo contrario, renderiza los datos actuales
        
   
        
    transformaciones = {
        'par_vars_segmento': cambiarAstring,
        
    }
    
    @reactive.effect
    @reactive.event(input.par_vars_segmento)
    def ver_input():
        valor1 = input.par_vars_segmento()
        trans_formara_lista = list(valor1)
        list_transformada.set(trans_formara_lista)
    
    
    @ui.bind_task_button(button_id="execute_in_sample")
    @reactive.extended_task
    async def ejecutar_in_sample_ascyn(click_count, mensaje, proceso):
        # Llamamos al método de la clase para ejecutar el proceso
        await modelo_in_sample.ejecutar_proceso_prueba(click_count, mensaje, proceso)
        
    ##Luego utilizo el input del id del boton para llamar ala funcion de arriba y que se ejecute con normalidad
    @reactive.effect
    @reactive.event(input.execute_in_sample, ignore_none=True)
    def ejecutar_in_sample_button():
        try:
            click_count_value = global_desarollo.click_counter.get()  # Obtener contador
            mensaje_value = global_desarollo.mensaje.get()  # Obtener mensaje actual
            proceso = global_desarollo.proceso.get()
            versiones = get_project_versions_param_mejorada(global_session.get_id_proyecto(), global_session.get_id_version())
            
            
            validar_ids = check_if_exist_id_version_id_niveles_scord(global_session.get_id_version(), global_session.get_version_parametros_id())
            if validar_ids:
                ui.modal_show(create_modal_generic("boton_advertencia_ejecute_in", f"Es obligatorio generar una versión de {global_name_in_Sample} y una versión para continuar."))
                return

            # Validar si hay versiones
            validacion_existe_modelo = verificar_estado_modelo_insa("Modeling_App.db", global_session.get_version_parametros_id(), global_session.get_id_dataSet())
            
            if validacion_existe_modelo:
               return ui.modal_show(create_modal_generic("close_button_insa_ok", f"Ya existe un modelo generado para la etapa {global_name_in_Sample}, en la versión {global_session.get_versiones_parametros_nombre()}"))
  
            
            if modelo_in_sample.pisar_el_modelo_actual.get() or validacion_existe_modelo is False:
                validator = Validator(input, global_session.get_data_set_reactivo(), name_suffix)
                
                if validator.is_valid():
                    inputs_procesados = {key: transformacion(input[key]()) for key, transformacion in transformaciones.items()}
                    rango_reportes = par_rango_reportes.data_view()
                    reportesMap = transformar_reportes(rango_reportes)
                    df_editado = par_rango_niveles.data_view()
                    
                    niveles_mapeados = transform_data(df_editado)

                    # Guardar los datos procesados
                    json_loader = LoadJson(input)
                    nuevos_valores = {
                        "delimiter_desarollo": global_estados.get_delimitador(),
                        "proyecto_nombre": global_session.get_name_proyecto(),
                        "par_rango_niveles": niveles_mapeados,
                        "par_rango_reportes": reportesMap,
                    }

                    # Actualizar el JSON con los nuevos valores
                    json_loader.update_values(nuevos_valores)
                    json_loader.save_json()

                    path_datos_entrada = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_entrada_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}/version_parametros_{global_session.get_version_parametros_id()}_{global_session.get_versiones_parametros_nombre()}'
                    path_datos_salida = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}/version_parametros_{global_session.get_version_parametros_id()}_{global_session.get_versiones_parametros_nombre()}'
                    
                    global_session.set_path_niveles_scorcads(path_datos_entrada)
                    global_session.set_path_niveles_scorcads_salida(path_datos_salida)

                    inputs_procesados = aplicar_transformaciones(input, transformaciones)
                    origen_modelo_puntoZip = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}'
                    
                    
                    movi = mover_file_reportes_puntoZip(origen_modelo_puntoZip, path_datos_entrada)
                    data_Set = get_datasets_directory(global_session.get_id_user(), global_session.get_id_proyecto(), global_session.get_name_proyecto())

                    mover_y_renombrar_archivo(global_names_reactivos.get_name_file_db(), data_Set, name_suffix, path_datos_entrada)

                    modelo_in_sample.porcentaje_path = path_datos_salida
                
                    modelo_in_sample.script_path = f"./Validar_Desa.sh --input-dir {path_datos_entrada} --output-dir {path_datos_salida}"
                    click.set(click() + 1)
                    ejecutar_in_sample_ascyn(click_count_value, mensaje_value, proceso)
                    modelo_in_sample.pisar_el_modelo_actual.set(False)
                else:
                    mensaje_de_error.set("\n".join(validator.get_errors()))
                    no_error.set(False)
                    mensaje.set("")


        except ValueError as e:
            mensaje.set(f"Error en la ejecución: {str(e)}")
        except Exception as e:
            mensaje.set(f"Error inesperado: {str(e)}")        
        
    def agregar_reactivo():  
        @reactive.effect
        def insert_data_depends_value():  
            if modelo_in_sample.proceso_ok.get():
                registro_id = agregar_datos_model_execution_por_json_version(
                    json_version_id=global_session.get_version_parametros_id(),
                    name=modelo_in_sample.nombre,
                    nombre_dataset=global_names_reactivos.get_name_file_db(),
                    estado="Exito",
                    dataset_id=global_session.get_id_dataSet()
                
                )
                estado_in_sample , hora_in_sample, mensaje_error = procesar_etapa_in_sample_2(base_datos="Modeling_App.db",  json_version_id=global_session.get_version_parametros_id(), etapa_nombre="in_sample")
                global_session_modelos.modelo_in_sample_estado.set(estado_in_sample)
                global_session_modelos.modelo_in_sample_hora.set(hora_in_sample)
                modelo_in_sample.proceso_ok.set(False)
                
            if modelo_in_sample.proceso_fallo.get():
                registro_id = agregar_datos_model_execution_por_json_version(
                    json_version_id=global_session.get_version_parametros_id(),
                    name=modelo_in_sample.nombre,
                    nombre_dataset=global_names_reactivos.get_name_file_db(),
                    estado="Error",
                     dataset_id=global_session.get_id_dataSet(),
                    mensaje_error=modelo_in_sample.mensaje.get()
                )
                estado_in_sample , hora_in_sample, mensaje_error = procesar_etapa_in_sample_2(base_datos="Modeling_App.db",  json_version_id=global_session.get_version_parametros_id(), etapa_nombre="in_sample")
                global_session_modelos.modelo_in_sample_estado.set(estado_in_sample)
                global_session_modelos.modelo_in_sample_hora.set(hora_in_sample)
                global_session_modelos.modelo_in_sample_mensaje_error.set(mensaje_error)                
                modelo_in_sample.proceso_fallo.set(False),
        
    agregar_reactivo()        
    
    
    
    
    @reactive.Effect
    @reactive.event(input.cancel_overwrite_in_sample)
    def modal_():
         return  ui.modal_remove()
    
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

    
    
    @reactive.Effect
    @reactive.event(input["continuar_no_overwrite_in_sample"])
    def valid_model_in_sample():
        modelo_in_sample.pisar_el_modelo_actual.set(True)
        return  ui.modal_remove()
    
    @reactive.effect
    @reactive.event(input.boton_advertencia_ejecute_in)
    def ok_in():
        return ui.modal_remove()
    
    @output
    @render.ui
    def card_in_sample():
        return   retornar_card(
        get_file_name=global_names_reactivos.get_name_file_db(),
        modelo=modelo_in_sample,
        fecha=global_session_modelos.modelo_in_sample_hora.get(),
        estado=global_session_modelos.modelo_in_sample_estado.get(),
        mensaje_error=global_session_modelos.modelo_in_sample_mensaje_error.get()
    )
    
    
    
    @reactive.calc
    def leer_archivo():
        """Lee el archivo de progreso y actualiza la UI."""
        if click.get() < 1:
            return ""
        
        if modelo_in_sample.proceso_fallo.get():
            return

        path_datos_salida = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}/version_parametros_{global_session.get_version_parametros_id()}_{global_session.get_versiones_parametros_nombre()}'
        name_file = "progreso.txt"

        # Obtener el último porcentaje del archivo
        ultimo_porcentaje = monitorizar_archivo(path_datos_salida, nombre_archivo=name_file)

        if ultimo_porcentaje == "100%":  # Si ya llegó al 100%, detener actualización
            print("Proceso completado. No se seguirá actualizando.")
            return "100%"

        # Actualizar variable reactiva
        modelo_in_sample.file_reactivo.set((ultimo_porcentaje))

        # Reactivar cada 3 segundos si aún no ha llegado al 100%
        reactive.invalidate_later(3)

        return ultimo_porcentaje

    # Mostrar el contenido del archivo en la UI
    @render.ui
    def value_in_sample():
        if click.get() >= 1:
            return f"Porcentaje: {leer_archivo()}"
    