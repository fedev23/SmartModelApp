# create_parameters

from shiny import App, Inputs, Outputs, Session, reactive, ui, render, module
from funciones.help_parametros.valid_columns import replace_spaces_with_underscores
from api import *
from clases.global_modelo import modelo_in_sample
from logica_users.utils.manejo_session import manejo_de_ultimo_seleccionado, generar_paths_insa, manejo_de_ultimo_seleccionado_niveles_ScoreCards
from funciones.utils import mover_file_reportes_puntoZip
from global_names import global_name_in_Sample
from clases.global_session import global_session
from api.db.sqlite_utils import *
from funciones.funciones_user import create_modal_v2, create_modal_versiones_param, button_remove
from api.db import *
from funciones_modelo.bd_tabla_validacion_sc import  obtener_ultimo_id_scoring_por_id_data_y_version
from clases.global_sessionV2 import *
from clases.global_sessionV3 import *
from funciones.utils_2 import crear_carpeta_version_parametros
from logica_users.utils.help_versios import obtener_opciones_versiones, obtener_ultimo_id_version, eliminar_carpeta, mapear_valor_a_clave
from datetime import datetime
from funciones_modelo.warning_model import verificar_estado_modelo_insa
from api.db.up_date import *
from funciones.utils_cargar_json import leer_control_json_in_sample
from auth.utils import help_api 
from funciones_modelo.global_estados_model import global_session_modelos
from funciones_modelo.help_models import *
from funciones_modelo.global_estados_model import global_session_modelos
from funciones.validacionY_Scoring.consultas import comparar_ultimo_file_por_ejecucion

def in_sample_verions(input: Inputs, output: Outputs, session: Session, name_para_button):
    
    lista = reactive.Value(None)
    id_versiones_params = reactive.Value(None)
    opciones_param = reactive.Value(None)
    valor_predeterminado_parms = reactive.Value(None)
    ultimo_id_reactivo = reactive.Value()
    nombre_de_la_version_in_sample = reactive.Value("")
    initialized = reactive.Value(False)
    is_initializing = reactive.Value(True)
    mensaje_error_tablero = reactive.Value()
    data_predeterminado = reactive.Value()
        
    

    @reactive.effect
    @reactive.event(input.create_parameters)
    def modal():
        return create_modal_versiones_param(global_session.get_name_proyecto(), global_session.get_versiones_name())

    @reactive.effect
    @reactive.event(input.continuar_version_param)
    def ok_verions():
        name = input['name_version_param']()
        current_timestamp = datetime.now().strftime("%Y-%m-%d %H")
        table_name = "json_versions"
        columns = ["nombre_version", "fecha_de_carga", "version_id"]
        values = [name,  current_timestamp, global_session.get_id_version()]  # Ejemplo: nombre de versión, fecha de carga y version_id
        add = insert_into_table(table_name, columns, values)
        global_session.set_version_parametros_id(add)
        id_versiones_params.set(add)
        obtener_nombre_version_por_id(global_session.get_id_version())
        name = replace_spaces_with_underscores(name)
        crear_carpeta_version_parametros(global_session.get_id_user(), global_session.get_id_proyecto(), global_session.get_id_version(), global_session.get_version_parametros_id(), name, global_session.get_name_proyecto(), global_session.get_versiones_name())

        ##ACTUALIZO ACA TAMBIEN EL SELECTOR YA QUE SI LO HAGO ACA CUANDO PONEN CONTINUAR LE DA LA ULT VERSION
        versiones_parametros = get_project_versions_param_mejorada(global_session.get_id_proyecto(), global_session.get_id_version())
        opciones_param.set(obtener_opciones_versiones(versiones_parametros, "id_jsons", "nombre_version")) 
        valor_predeterminado_parms.set(obtener_ultimo_id_version(versiones_parametros, "id_jsons"))
        
        ui.update_select("version_selector",choices=opciones_param.get(), selected=valor_predeterminado_parms.get())
        
        ui.modal_remove()
        
    @reactive.effect
    @reactive.event(input.cancelar_version_param)
    def Ko_verions():
        ui.modal_remove()
    
    
        
    @reactive.effect
    @reactive.event(input.version_selector)
    def seleccionador_versiones_param():
        base_datos = "Modeling_App.db"
        ultimo_id_reactivo.set(obtener_ultimo_id_seleccionado(base_datos, "json_versions", "id_jsons"))
        versiones_parametros  = get_project_versions_param_mejorada(global_session.get_id_proyecto(), global_session.get_id_version())
        
        ##obtengo el ultima version seleccionada por el usario.
        manejo_de_ultimo_seleccionado_niveles_ScoreCards(
            is_initializing=is_initializing,
            input_select_value=input.version_selector(),
            ultimo_id_func=lambda: obtener_ultimo_id_seleccionado_edited(base_datos, "json_versions", "id_jsons", global_session.get_id_version()),
            global_set_func=lambda x: global_session.set_version_parametros_id(x),
            actualizar_ultimo_func=lambda table, column, value: actualizar_ultimo_seleccionado_new(base_datos, table, column, value, global_session.get_id_version()),
            obtener_ultimo_func=lambda table, column: obtener_ultimo_seleccionado(base_datos, table, column),
            obtener_opciones_func=lambda: obtener_opciones_versiones(versiones_parametros, "id_jsons", "nombre_version"),
            mapear_clave_func=mapear_valor_a_clave, 
            ui_update_func=lambda name, choices, selected: ui.update_select(name, choices=choices, selected=selected),
            input_select_name="version_selector",
            db_table="json_versions",
            db_column_id="id_jsons",
            db_column_name="nombre_version",
            db="Modeling_App.db"
        )
        
        
        nombre_files_validacion_sc = obtener_nombres_files_por_proyecto(global_session.get_id_proyecto())
        global_session_V2.set_opciones_name_dataset_Validation_sc(obtener_opciones_versiones(nombre_files_validacion_sc, "id_nombre_file", "nombre_file"))
        ##OBTENGO EL ULTIMO NOMBRE FILES SELECCIONADO EN FULL
        ultimo_id_file_seleccionado_validacion_full_o_scoring = comparar_ultimo_file_por_ejecucion(global_session.get_version_parametros_id())
        if ultimo_id_file_seleccionado_validacion_full_o_scoring:
            data_predeterminado.set(ultimo_id_file_seleccionado_validacion_full_o_scoring)
        else:
            data_predeterminado.set(obtener_ultimo_id_version(nombre_files_validacion_sc, 'id_nombre_file'))

       
        ui.update_select("files_select_validation_scoring",choices=global_session_V2.get_opciones_name_dataset_Validation_sc(), selected=data_predeterminado.get())
                    
        if not initialized():
            initialized.set(True)
            return 
        
        global_session_V2.click_seleccion_niveles_score.set(global_session_V2.click_seleccion_niveles_score() + 1)
        if global_session_V2.click_seleccion_niveles_score.get() >=1:
            
            versiones_id = input.version_selector()
            global_session.set_version_parametros_id(versiones_id)
            ultimo_id_validacion_score = obtener_ultimo_id_de_validacion_full_por_id_data_y_version(global_session_V2.get_id_Data_validacion_sc(), global_session.get_version_parametros_id())
            
            ultimo_id_score = obtener_ultimo_id_scoring_por_id_data_y_version(global_session_V2.get_id_Data_validacion_sc(), global_session.get_version_parametros_id())
            
            if ultimo_id_validacion_score:  # Verifica si hay un registro válido
                global_session_V3.id_validacion_scoring.set(ultimo_id_validacion_score)
            else:
                global_session_V3.id_validacion_scoring.set(None)
                
            ##OBTENOG EL ULTIMO ID SE SOCORE
            if ultimo_id_score:
                global_session_V3.id_score.set(ultimo_id_score)
            else:
                global_session_V3.id_score.set(None)
              

            if global_session.get_version_parametros_id() != "a":
                versiones = get_project_versions_param_mejorada(global_session.get_id_proyecto(), global_session.get_id_version())
                if versiones:
                    if (global_session.get_id_user() and
                    global_session.get_name_proyecto() and
                    global_session.get_id_proyecto() and
                    global_session.get_id_version() and
                    global_session.get_versiones_name() and 
                    global_session.get_version_parametros_id() and
                    global_session.get_versiones_parametros_nombre()):   
                        help_api.procesar_starlette_api_insample(global_session.get_id_user(), global_session.get_name_proyecto(), global_session.get_id_proyecto(), global_session.get_id_version(), global_session.get_versiones_name(), global_session.get_version_parametros_id(), global_session.get_versiones_parametros_nombre())

                        #ult_model = obtener_ultimo_modelo_por_version(base_datos="Modeling_App.db",version_id=None, json_version_id=global_session.get_version_parametros_id())
                        #print(ult_model, "viendo si duelve bien el diccionario") 
                        if opciones_param.get() is  None:
                            nombre_version = versiones[0]['nombre_version']
                            nombre_de_la_version_in_sample.set(nombre_version)
                            nombre_version_niveles_score = obtener_valor_por_id_versiones(global_session.get_version_parametros_id())
                            global_session.set_versiones_parametros_nombre(replace_spaces_with_underscores(nombre_version_niveles_score))
                            global_session_V3.name_version_niveles_score_original.set(nombre_version_niveles_score)
                            
                    
                nombre_version_niveles_Scord = obtener_valor_por_id_versiones(global_session.get_version_parametros_id())
                
                global_session_V3.name_version_niveles_score_original.set(nombre_version_niveles_Scord)
                global_session.set_versiones_parametros_nombre(replace_spaces_with_underscores(nombre_version_niveles_Scord))
                estado_in_sample , hora_in_sample, mensaje_error = procesar_etapa_in_sample_2(base_datos="Modeling_App.db", json_version_id=global_session.get_version_parametros_id(), etapa_nombre="in_sample")
        
                
                global_session_modelos.modelo_in_sample_estado.set(estado_in_sample)
                global_session_modelos.modelo_in_sample_hora.set(hora_in_sample)
                global_session_modelos.modelo_in_sample_mensaje_error.set(mensaje_error)
                
                
                param_json_in_sample = leer_control_json_in_sample(global_session.get_id_user(), global_session.get_id_proyecto(), global_session.get_name_proyecto(), global_session.get_id_version(), global_session.get_versiones_name(), global_session.get_versiones_parametros_nombre(), global_session.get_version_parametros_id())
                print(f"llegando hasta aca? {param_json_in_sample}")
                global_session_V3.json_params_insa.set(param_json_in_sample)
                
            
    
    
        
    @output
    @render.ui
    def button_remove_versions_params():
        versions_list = get_project_versions_param_mejorada(global_session.get_id_proyecto(), global_session.get_id_version())
        name = global_session.get_versiones_name()
        return button_remove(versions_list, global_session.get_version_parametros_id(), "id_jsons", name)
    
    
    delete_button_effects = {}  # Diccionario para rastrear los efectos ya definidos

    @reactive.Effect
    def handle_delete_buttons():
        # Obtener y preparar el identificador único para el botón
        name = replace_spaces_with_underscores(global_session.get_versiones_name())
        eliminar_btn_id = f"eliminar_version_{global_session.get_version_parametros_id()}_{name}"

        # Verificar si el efecto ya está registrado
        if eliminar_btn_id not in delete_button_effects:
            print(f"Registrando efecto para botón: {eliminar_btn_id}")

            # Lógica para manejar el evento del botón
            def eliminar_param_boton():
                print("Eliminando niveles y scoring para:", name)
                create_modal_v2(
                    f"Eliminar versión de {global_name_in_Sample}, {name}?",
                    "Confirmar",
                    "Cancelar",
                    "confirmar_remove",
                    "cancelar_remove_niveles_sc"
                )

            # Registrar el evento para el botón
            @reactive.Effect
            @reactive.event(input[eliminar_btn_id])
            def manejar_eliminar_boton():
                eliminar_param_boton()

            # Guardar el efecto en el diccionario
            delete_button_effects[eliminar_btn_id] = manejar_eliminar_boton
        else:
            print(f"Efecto ya registrado para botón: {eliminar_btn_id}")
    
        
    @reactive.Effect
    @reactive.event(input.confirmar_remove)
    def remove_versiones_de_parametros():
        eliminar_version("json_versions", "id_jsons", global_session.get_version_parametros_id())
        name_sin_espacios = replace_spaces_with_underscores(global_session.get_versiones_parametros_nombre())
        path_carpeta_versiones_borrar_entrada = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_entrada_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}/version_parametros_{global_session.get_version_parametros_id()}_{global_session.get_versiones_parametros_nombre()}'
        path_carpeta_versiones_borrar_salida = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}/version_parametros_{global_session.get_version_parametros_id()}_{global_session.get_versiones_parametros_nombre()}'
            
        eliminar_carpeta(path_carpeta_versiones_borrar_salida)
        eliminar_carpeta(path_carpeta_versiones_borrar_entrada)
        
        columnas = ['id_jsons', 'nombre_version', 'fecha_de_carga']
        tabla = "json_versions"
        condiciones = "version_id = ?"
        parametros = (global_session.get_id_version(),)  
        lista_de_versiones_new = obtener_versiones_por_proyecto(columnas,tabla, condiciones,parametros)
        lista.set(lista_de_versiones_new)
        ui.update_select(
            "version_selector",
            choices={str(vers['id_jsons']): vers['nombre_version']
                     for vers in lista_de_versiones_new}
        )
        return ui.modal_remove()
    
    
    
    @reactive.effect
    @reactive.event(input.cancelar_remove_niveles_sc)    
    def remove_Versiones_niveles_scord():
        return ui.modal_remove()
        
     
        


    @reactive.effect
    def update_nav():
        base_datos = "Modeling_App.db"
        if global_session_V2.click_seleccion_niveles_score.get() >1:
            
            if isinstance(ultimo_id_reactivo.get(), tuple):
                ultimo_id_reactivo.set(ultimo_id_reactivo.get()[0]) 
                print(ultimo_id_reactivo.get())
        
            id_actual = input.version_selector()
            id_actual = int(id_actual)
            
                
            if ultimo_id_reactivo.get() != id_actual:
                ui.update_navs("navset", selected="screen_niveles_scorcads")  # Cambia al panel deseado
                global_session_V2.click_seleccion_niveles_score.set(0)
                
                
    
    @output
    @render.ui
    def tablero_in_sample():
        validacion_existe_modelo = verificar_estado_modelo_insa("Modeling_App.db", global_session.get_version_parametros_id(), global_session.get_id_dataSet())
        if validacion_existe_modelo or modelo_in_sample.proceso_ok.get():
            return ui.input_action_link("tablero_in_sample", "Ver tablero de reportes")
    
    
    @reactive.effect
    @reactive.event(input.tablero_in_sample)
    async def rederic_tablero():
        entrada, salida = generar_paths_insa(global_session)
        movi = mover_file_reportes_puntoZip(salida, entrada)
                   
        modelo_in_sample.script_path_tablero = f"./Tablero_IVs.sh --input-dir {entrada} --output-dir {salida}"
        return_code = await modelo_in_sample.run_script_tablero()

        # Redirigir solo si el script se ejecutó correctamente (código 0 = éxito)
        if return_code == 0:
            session.send_custom_message("redirect", "http://localhost:3838")
        else:
            mensaje_error_tablero.set("Hubo un problema con la redirigimiento")
        