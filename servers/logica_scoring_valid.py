from shiny import reactive, render, ui
from global_var import global_data_loader_manager
from funciones.utils_2 import render_data_summary
from clases.global_modelo import modelo_of_sample
from clases.global_session import global_session
from api.db import *
from clases.reactives_name import global_names_reactivos
from funciones.utils import retornar_card
from shiny.types import FileInfo
from datetime import datetime
from funciones.funciones_cargaDatos import guardar_archivo
from funciones.help_versios import obtener_opciones_versiones, obtener_ultimo_id_version, obtener_ultimo_nombre_archivo
from clases.global_sessionV2 import *
from funciones.utils_2 import leer_dataset
import pandas as pd
from funciones.funciones_user import button_remove, create_modal_v2
from clases.global_modelo import modelo_of_sample, modelo_produccion



def logica_server_Validacion_scroing(input, output, session, name_suffix):
    
    dataSet_predeterminado_parms = reactive.Value(None)
    global_names_reactivos.name_validacion_of_to_sample_set(name_suffix)
    validadacion_retornar_card = reactive.Value("")
    data_predeterminado = reactive.Value("")
    files_name  = reactive.Value("")
    lista = reactive.Value("")
    reactivo_dinamico =  reactive.Value("")
    
    @reactive.Effect
    @reactive.event(input.file_validation)
    async def loadOutSample():
        try:
            file: list[FileInfo] | None = input.file_validation()
            if not file:
                raise ValueError("No se recibió ningún archivo para validar.")

            print(file, "estoy en fila")
            input_name = file[0]['name']
            print(f"Nombre del archivo recibido: {input_name}")

            # Guardar el archivo
            name_suffix = "_validation"  # Ejemplo de sufijo, ajusta según sea necesario
            ruta_guardado = await guardar_archivo(input.file_validation, name_suffix)
            print(f"El archivo fue guardado en {ruta_guardado}")

            # Obtener fecha actual
            fecha_de_carga = datetime.now().strftime("%Y-%m-%d %H:%M")

            # Insertar datos en la tabla
            id = insert_into_table(
                "validation_scoring",
                ['nombre_archivo_validation_sc', 'fecha_de_carga', 'project_id', 'version_id'],
                [input_name, fecha_de_carga, global_session.get_id_proyecto(), global_session.get_id_version()]
            )
            print("Datos insertados en la tabla validation_scoring.")
            global_session_V2.set_id_Data_validacion_sc(id)
            # Extraer datos
            files_name.set(get_records(
                table='validation_scoring',
                columns=['id_validacion_sc', 'nombre_archivo_validation_sc', 'fecha_de_carga'],
                where_clause='project_id = ?',
                where_params=(global_session.get_id_proyecto(),)
            ))
            # Actualizar opciones y seleccionar predeterminados
            global_session_V2.set_opciones_name_dataset_Validation_sc(obtener_opciones_versiones(files_name.get(), "id_validacion_sc", "nombre_archivo_validation_sc"))
            data_predeterminado.set(obtener_ultimo_id_version(files_name.get(), "id_validacion_sc"))
            
            
            ui.update_select(
                "files_select_validation_scoring",
                choices=global_session_V2.get_opciones_name_dataset_Validation_sc(),
                selected=data_predeterminado.get()
            )
            print("Opciones y selección actualizadas correctamente.")

        except Exception as e:
            # Manejar errores y notificar al usuario
            error_message = f"Error en loadOutSample: {e}"
            #ui.update_text("error_message", error_message)  # Asume que hay un output de texto para mostrar errores
            print(error_message)
    
      

    @reactive.Effect
    @reactive.event(input.files_select_validation_scoring)
    def seleccionador():
        #PREPARO LA CONSULTA
        data_id = input.files_select_validation_scoring()  # Captura el ID seleccionado
        global_session_V2.set_id_Data_validacion_sc(data_id)
        base_datos = 'Modeling_App.db'
        tabla = 'validation_scoring'
        columna_objetivo = 'nombre_archivo_validation_sc'
        columna_filtro = 'id_validacion_sc'
        nombre_file = obtener_valor_por_id(base_datos, tabla, columna_objetivo, columna_filtro, global_session_V2.get_id_Data_validacion_sc())
        
        global_session_V2.set_nombre_dataset_validacion_sc(nombre_file)
        
        ##obengo los valores de la tabla
        lista.set(get_records(table='validation_scoring',
                columns=['id_validacion_sc', 'nombre_archivo_validation_sc', 'fecha_de_carga'],
                where_clause='project_id = ?',
                where_params=(global_session.get_id_proyecto(),)))
        
        if global_session_V2.get_nombre_dataset_validacion_sc() is None:
            dataSet_predeterminado_parms.set(obtener_ultimo_nombre_archivo(lista.get()))
        else:
            dataSet_predeterminado_parms.set(global_session_V2.get_nombre_dataset_validacion_sc())
        
        data = leer_dataset(global_session.get_id_user(), global_session.get_id_proyecto(), global_session.get_name_proyecto(), dataSet_predeterminado_parms.get())
        global_session_V2.set_data_set_reactivo_validacion_sc(data)
        ##actualizo el selector de columna target
    
    
    ##BOTON PARA REMOVER DATASET
    @output
    @render.ui
    def remove_dataset_data_alidacionSC():
        lista_2_borrar = (get_records(table='validation_scoring',
            columns=['id_validacion_sc', 'nombre_archivo_validation_sc', 'fecha_de_carga'],
            where_clause='project_id = ?',
            where_params=(global_session.get_id_proyecto(),)))
        #name.set(global_names_reactivos.get_name_file_db())
        #print(lista_2_borrar, "estoy en lista dos de borrar")
        return button_remove(lista_2_borrar, global_session_V2.get_id_Data_validacion_sc(), "id_validacion_sc", name_suffix)
    
    
    @reactive.Effect
    def boton_para_eliminar_name_data_set_validacion_sc():
        eliminar_version_id = f"eliminar_version_{global_session_V2.get_id_Data_validacion_sc()}_{name_suffix}"

        @reactive.Effect
        @reactive.event(input[eliminar_version_id])
        def eliminar_version_id():
            base_datos = 'Modeling_App.db'
            tabla = 'validation_scoring'
            columna_objetivo = 'nombre_archivo_validation_sc'
            columna_filtro = 'id_validacion_sc'
            nombre_version = obtener_valor_por_id(base_datos, tabla, columna_objetivo, columna_filtro, global_session_V2.get_id_Data_validacion_sc())
            #nombre_version = obtener_valor_por_id(global_session.get_id_dataSet())
            create_modal_v2(f"Seguro que quieres eliminar el Dataset {nombre_version}?", "Confirmar", "Cancelar", "confirmar_id_borrar_dataset_validacion_Sc", "cancelar_id_dataSet_validacion_Sc")
    
    @reactive.Effect
    @reactive.event(input["confirmar_id_borrar_dataset_validacion_Sc"])
    def remove_modal_Dataset():
        ui.modal_remove()     
     
     
    @reactive.Effect
    @reactive.event(input.confirmar_id_borrar_dataset_validacion_Sc)
    def remove_versiones_de_parametros():
        eliminar_version("validation_scoring", "id_validacion_sc", global_session_V2.get_id_Data_validacion_sc())
        columnas = ['id_validacion_sc', 'nombre_archivo_validation_sc']
        lista_de_versiones_new = obtener_versiones_por_proyecto(global_session.get_id_proyecto(), columnas, "validation_scoring", "project_id")
        lista.set(lista_de_versiones_new)
        ui.update_select(
            "files_select_validation_scoring",
            choices={str(vers['id_validacion_sc']): vers['nombre_archivo_validation_sc']
                     for vers in lista_de_versiones_new}
        )
        ui.modal_remove()   
  
  
    
    @output
    @render.data_frame
    def summary_data_validacion_out_to_sample():
        return render_data_summary(global_session_V2.get_data_reactivo_validacion_sc())


    @reactive.Effect
    @reactive.event(input.radio_models)
    def seleccionador_de_radio_button():
        input_radio = input.radio_models()
        print(input_radio, "estoy en radio")
        validadacion_retornar_card.set(input_radio)
      
        
        
    @output
    @render.ui
    def card_out_to_sample():
        if validadacion_retornar_card.get()== "1":
            return  retornar_card(
                #prin(get_data_reactivo_validacion_sc)
            get_file_name=global_session_V2.get_nombre_dataset_validacion_sc(),
            #get_fecha=global_fecha.get_fecha_of_to_Sample,
            modelo=modelo_of_sample)
        else:
              return ui.div()
            
    
    @output
    @render.ui
    def seleccionador_target():
        # Reactivo para verificar el valor del radio botón y actualizar dinámicamente
        @reactive.Effect
        def handle_radio_change():
            if validadacion_retornar_card.get() == "1":
                # Actualiza la lista de registros
                lista.set(get_records(
                    table='validation_scoring',
                    columns=['id_validacion_sc', 'nombre_archivo_validation_sc', 'fecha_de_carga'],
                    where_clause='project_id = ?',
                    where_params=(global_session.get_id_proyecto(),)
                ))

                # Determina el dataset predeterminado o usa uno existente
                if global_session_V2.get_nombre_dataset_validacion_sc() is None:
                    dataSet_predeterminado_parms.set(
                        obtener_ultimo_nombre_archivo(lista.get())
                    )
                else:
                    dataSet_predeterminado_parms.set(
                        global_session_V2.get_nombre_dataset_validacion_sc()
                    )

                # Leer el dataset y actualizar datos globales
                data = leer_dataset(
                    global_session.get_id_user(),
                    global_session.get_id_proyecto(),
                    global_session.get_name_proyecto(),
                    dataSet_predeterminado_parms.get()
                )
                global_session_V2.set_data_set_reactivo_validacion_sc(data)

                # Verificar si el dataset es válido y obtener nombres de columnas
                if isinstance(data, pd.DataFrame) and not data.empty:
                    column_names = data.columns.tolist()
                else:
                    column_names = []

                # Actualizar el selector con las columnas disponibles
                ui.update_selectize("selectize_columnas_target", choices=column_names)
        
        # Devuelve el selector con opciones dinámicamente actualizadas
        if validadacion_retornar_card.get() == "1":
            return ui.input_selectize(
                "selectize_columnas_target",
                "",
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
            

    @output
    @render.ui
    def card_produccion1():
        if  reactivo_dinamico.get() == "2":
            return retornar_card(
                get_file_name=global_session_V2.get_nombre_dataset_validacion_sc(),
                #get_fecha=global_fecha.get_fecha_produccion,
                modelo=modelo_produccion
            )
    
