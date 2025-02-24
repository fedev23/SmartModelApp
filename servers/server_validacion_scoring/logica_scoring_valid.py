from shiny import reactive, render, ui
from funciones.utils_2 import render_data_summary, eliminar_archivo, leer_dataset, get_datasets_directory, get_folder_directory_data_validacion_scoring_SALIDA
from clases.global_modelo import modelo_of_sample
from clases.global_session import global_session
from api.db import *
from funciones.help_parametros.valid_columns import *
from auth.utils import help_api
from clases.global_sessionV3 import *
from clases.reactives_name import global_names_reactivos
from funciones.utils import retornar_card
from logica_users.utils.help_versios import obtener_ultimo_nombre_archivo_validacion_c
from clases.global_sessionV2 import *
import pandas as pd
from api.db.up_date import *
from funciones_modelo.bd_tabla_validacion_sc import *
from funciones_modelo.help_models import *
from funciones_modelo.warning_model import validar_existencia_modelo_por_dinamica_de_app, obtener_nombre_dataset
from clases.global_modelo import global_desarollo
from funciones.funciones_user import button_remove, create_modal_v2
from funciones_modelo.global_estados_model import global_session_modelos
from funciones.clase_estitca.cargar_files import FilesLoad
import os
from funciones.validacionY_Scoring.consultas import comparar_ultimo_file_por_ejecucion
from funciones.utils_cargar_json import update_selectize_from_columns_and_json
from clases.global_modelo import modelo_of_sample, modelo_produccion




def logica_server_Validacion_scroing(input, output, session, name_suffix):
    cargar_datos_class = FilesLoad(name_suffix)
    
    dataSet_predeterminado_parms = reactive.Value(None)
    global_names_reactivos.name_validacion_of_to_sample_set(name_suffix)
    validadacion_retornar_card = reactive.Value("")
    lista = reactive.Value("")
    reactivo_dinamico =  reactive.Value("")
    modelo_existe = reactive.Value(False)
    
    
    
    @reactive.Effect
    @reactive.event(input.file_validation)
    async def loadOutSample():
        await cargar_datos_class.cargar_datos_validacion_scroing(input.file_validation)
    
    
      

    @reactive.Effect
    @reactive.event(input.files_select_validation_scoring)
    async def seleccionador():
        #PREPARO LA CONSULTA
        data_id = input.files_select_validation_scoring()  # Captura el ID seleccionado
        global_session_V2.set_id_Data_validacion_sc(data_id)
        base_datos = 'Modeling_App.db'
        nombre_file =  obtener_nombre_file(base_datos, data_id)

        global_session_V2.set_nombre_dataset_validacion_sc(nombre_file)
        if nombre_file:
            file_name_without_extension = os.path.splitext(nombre_file)[0]
            global_session_V2.nombre_file_sin_extension_validacion_scoring.set(file_name_without_extension)
        ##obengo los valores de la tabla
        
        ultimo_id_score = obtener_ultimo_id_scoring_por_id_data_y_version(global_session_V2.get_id_Data_validacion_sc(), global_session.get_version_parametros_id())
     
        if ultimo_id_score:
                global_session_V3.id_score.set(ultimo_id_score)
        else:
                global_session_V3.id_score.set(None)
                
        
        lista.set(obtener_nombres_files_por_proyecto(global_session.get_id_proyecto()))
        
        global_session_V3.id_validacion_scoring.set(obtener_ultimo_id_de_validacion_full_por_id_data_y_version(global_session_V2.get_id_Data_validacion_sc(), global_session.get_version_parametros_id()))
        
        #EL PARAMETRO DE PISAR EL MODELO ACTUAL NO ESTA EN USO POR EL MOMENTO, ESTA HECHO POR SI EN UN MOMENTO SE LE DA LA OPCION DEL USER DE PISAR EL MODELO GENERADO
        modelo_existente = validar_existencia_modelo_por_dinamica_de_app(
                modelo_boolean_value=global_desarollo.pisar_el_modelo_actual.get(),
                base_datos=base_datos,
                nombre_modelo=modelo_of_sample.nombre,
                id_validacion_score=global_session_V2.get_id_Data_validacion_sc()
            )
        
        
        if global_session_V2.get_nombre_dataset_validacion_sc() is None:
            dataSet_predeterminado_parms.set(obtener_ultimo_nombre_archivo_validacion_c(lista.get()))
            
        if modelo_existente:
            nombre_modelo_usado = obtener_nombre_dataset(global_session.get_version_parametros_id())
            modelo_existe.set(True)
            global_session_V2.set_nombre_dataset_validacion_sc(nombre_modelo_usado)
            
         
            
        
        if (global_session.get_id_user() and
                global_session.get_name_proyecto() and
                global_session.get_id_proyecto() and
                global_session.get_id_version() and
                global_session.get_versiones_name() and 
                global_session_V2.nombre_file_sin_extension_validacion_scoring.get()): 
                    await help_api.procesar_starlette_api_validacion_scoring(global_session.get_id_user(), global_session.get_name_proyecto(), global_session.get_id_proyecto(), global_session.get_id_version(), global_session.get_versiones_name(), global_session.get_version_parametros_id(), global_session.get_versiones_parametros_nombre(), global_session_V2.nombre_file_sin_extension_validacion_scoring.get())

        
        #data = leer_dataset_sc(global_session.get_id_user(), global_session.get_id_proyecto(), global_session.get_name_proyecto(), global_session_V2.get_nombre_dataset_validacion_sc())
        #ui.update_select("files_select_validation_scoring",choices=global_session_V2.get_opciones_name_dataset_Validation_sc(), selected=dataSet_predeterminado_parms.get())
        data = leer_dataset(
            global_session.get_id_user(),
            global_session.get_id_proyecto(),
            global_session.get_name_proyecto(),
            global_session_V2.get_nombre_dataset_validacion_sc(),
            global_session.get_versiones_name(),
            global_session.get_id_version()
        )
        global_session_V2.set_data_set_reactivo_validacion_sc(data)
        
        ##actualizo el selector de columna target
    
    
    ##BOTON PARA REMOVER DATASET
    @output
    @render.ui
    def remove_dataset_data_alidacionSC():
        lista_2_borrar = (obtener_nombres_files_por_proyecto(global_session.get_id_proyecto()))
        return button_remove(lista_2_borrar, global_session_V2.get_id_Data_validacion_sc(), "id_nombre_file", name_suffix)
    
    
    delete_button_effects = {}
    @reactive.Effect
    def boton_para_eliminar_name_data_set_validacion_sc():
        eliminar_version_id = f"eliminar_version_{global_session_V2.get_id_Data_validacion_sc()}_{name_suffix}"
        if eliminar_version_id not in delete_button_effects:
            @reactive.Effect
            @reactive.event(input[eliminar_version_id])
            def elimanar_validacion_score():
                create_modal_v2(f"Seguro que quieres eliminar el Dataset {global_session_V2.get_nombre_dataset_validacion_sc()}?", "Confirmar", "Cancelar", "confirmar_id_borrar_dataset_validacion_Sc", "cancelar_id_dataSet_validacion_Sc")
            
            delete_button_effects[eliminar_version_id] = eliminar_version_id
        
    @reactive.Effect
    @reactive.event(input["cancelar_id_dataSet_validacion_Sc"])
    def remove_modal_Dataset():
        return ui.modal_remove()     
     
     
    @reactive.Effect
    @reactive.event(input.confirmar_id_borrar_dataset_validacion_Sc)
    def remove_versiones_de_parametros():
        eliminar_version("nombre_files", "id_nombre_file", global_session_V2.get_id_Data_validacion_sc())
        directorio = get_datasets_directory(
        global_session.get_id_user(), 
        global_session.get_id_proyecto(), 
        global_session.get_name_proyecto()
        )
        
        dataset_path = os.path.join(directorio, global_session_V2.get_nombre_dataset_validacion_sc())
        
        path_datos_salida  = get_folder_directory_data_validacion_scoring_SALIDA(global_session.get_id_user(), global_session.get_id_proyecto(), global_session.get_name_proyecto(), global_session.get_versiones_name(), global_session.get_id_version(), global_session.get_version_parametros_id(), global_session.get_versiones_parametros_nombre(), global_session_V2.nombre_file_sin_extension_validacion_scoring.get())
        eliminar_archivo(dataset_path)
        eliminar_archivo(path_datos_salida)
        lista_de_versiones_new = obtener_nombres_files_por_proyecto(global_session.get_id_proyecto())
        lista.set(lista_de_versiones_new)
        ui.update_select(
            "files_select_validation_scoring",
            choices={str(vers['id_nombre_file']): vers['nombre_file']
                     for vers in lista_de_versiones_new}
        )
        return ui.modal_remove()   
  
  
    
    @output
    @render.data_frame
    def summary_data_validacion_out_to_sample():
        data = global_session_V2.get_data_reactivo_validacion_sc()
        if data is None or data.empty:
            return None
        return render_data_summary(data)
        #return render_data_summary(global_session_V2.get_data_reactivo_validacion_sc())


    @reactive.Effect
    @reactive.event(input.radio_models)
    def seleccionador_de_radio_button():
        input_radio = input.radio_models()
        validadacion_retornar_card.set(input_radio)
        
        
        
    @output
    @render.ui
    def card_out_to_sample():
        if validadacion_retornar_card.get()== "1":
            if modelo_existe.get():
                nombre_modelo_usado = obtener_nombre_dataset(global_session.get_version_parametros_id())
                modelo_existe.set(True)
                global_session_V2.set_nombre_dataset_validacion_sc(nombre_modelo_usado)
            
            if global_session_V3.id_validacion_scoring.get() is not None:
                #global_session_V3.id_validacion_scoring.set(obtener_ultimo_id_de_validacion_full_por_id_data(global_session_V2.get_id_Data_validacion_sc()))
                estado_out_sample , hora_of_sample, mensaje_error = procesar_etapa_validacion_full(base_datos="Modeling_App.db", id_validacion_sc=global_session_V3.id_validacion_scoring.get(), id_file=global_session_V2.get_id_Data_validacion_sc(), etapa_nombre=modelo_of_sample.nombre)
                global_session_modelos.modelo_of_sample_estado.set(estado_out_sample)
                global_session_modelos.modelo_of_sample_hora.set(hora_of_sample)
                global_session_modelos.modelo_of_sample_error.set(mensaje_error)
                
            else:
                global_session_modelos.modelo_of_sample_estado.set("")
                global_session_modelos.modelo_of_sample_hora.set("")
                global_session_modelos.modelo_of_sample_error.set("")
            
                
            data = global_session_V2.get_data_reactivo_validacion_sc()
            if data is not None and not data.empty:
                return  retornar_card(
                get_file_name=global_session_V2.get_nombre_dataset_validacion_sc(),
                modelo=modelo_of_sample,
                fecha=global_session_modelos.modelo_of_sample_hora.get(),
                estado=global_session_modelos.modelo_of_sample_estado.get(),
                mensaje_error=global_session_modelos.modelo_of_sample_error.get())
                
            else:
               return ui.div()
        else:
              return ui.div()
            
    
    @output
    @render.ui
    def seleccionador_target():
        # Reactivo para verificar el valor del radio botón y actualizar dinámicamente
        @reactive.Effect
        def handle_radio_change():
            if validadacion_retornar_card.get() == "1":
                    # Evita bucles reactivos: verifica si el dataset ya está configurado
                data = global_session_V2.get_data_reactivo_validacion_sc()
                if data is not None and not data.empty:
                    # Actualiza la lista de registros solo si es necesario
                    column_names = get_binary_columns(data)
                    # Verificar si el dataset es válido y obtener nombres de columnas
                    if isinstance(data, pd.DataFrame) and not data.empty:
                        column_names = get_binary_columns(data)
                    else:
                        column_names = []
                    
                    # Actualizar el selector con las columnas disponibles
                    ui.update_selectize("selectize_columnas_target", choices=column_names)
                    
                    json_params = global_session_V2.get_json_params_desarrollo()
                    update_full = {"selectize_columnas_target" : "par_target"}
                    update_selectize_from_columns_and_json(column_names, update_full, json_params)
           
                    
         # Devuelve el selector con opciones dinámicamente actualizadas
        if validadacion_retornar_card.get() == "1":
            return ui.input_selectize(
                "selectize_columnas_target",
                "Seleccione la columna target",
                choices=[],
                multiple=False,
                options={"placeholder": "Seleccionar columna target."}
            )
        else:
            return None
    
    
    @reactive.Effect
    @reactive.event(input.radio_models)
    def seleccionador_de_radio_button():
        input_radio = input.radio_models()
        reactivo_dinamico.set(input_radio)
            
    
    @reactive.Effect
    @reactive.event(input.boton_advertencia_files)
    def button_cancel():
        return ui.modal_remove()
    

    @output
    @render.ui
    def card_produccion1():
        if  reactivo_dinamico.get() == "2":
            data = global_session_V2.get_data_reactivo_validacion_sc()
            if modelo_existe.get():
                    nombre_modelo_usado = obtener_nombre_dataset(global_session.get_version_parametros_id())
                    modelo_existe.set(True)
                    global_session_V2.set_nombre_dataset_validacion_sc(nombre_modelo_usado)
                 
            if global_session_V3.id_score.get() is not None:
                print(f"id socre {global_session_V3.id_score.get()}")
                print(f"id data en hay id score{global_session_V2.get_id_Data_validacion_sc()}")
                estado_produccion , hora_produccion, mensaje_error = procesar_etapa_validacion_scroing(base_datos="Modeling_App.db", id_score=global_session_V3.id_score.get(), id_nombre_file=global_session_V2.get_id_Data_validacion_sc(), etapa_nombre=modelo_produccion.nombre)
                global_session_modelos.modelo_produccion_estado.set(estado_produccion)
                global_session_modelos.modelo_produccion_hora.set(hora_produccion)
                global_session_modelos.modelo_desarrollo_mensaje_error.set(mensaje_error)
            else:
                global_session_modelos.modelo_produccion_estado.set("")
                global_session_modelos.modelo_produccion_hora.set("")
                global_session_modelos.modelo_desarrollo_mensaje_error.set("")
                
            if data is not None and not data.empty:
                return retornar_card(
                    get_file_name=global_session_V2.get_nombre_dataset_validacion_sc(),
                    #get_fecha=global_fecha.get_fecha_produccion,
                    modelo=modelo_produccion,
                    fecha=global_session_modelos.modelo_produccion_hora.get(),
                    estado=global_session_modelos.modelo_produccion_estado.get(),
                    mensaje_error=global_session_modelos.modelo_produccion_error.get(   )
                )
    

    @reactive.Effect
    @reactive.event(input.boton_advertencia_ejecute_of)
    def button_cancel():
        return ui.modal_remove()
    
    
    @reactive.Effect
    @reactive.event(input.boton_advertencia_ejecute_produccion)
    def button_cancel():
        return ui.modal_remove()
    