from shiny import App, Inputs, Outputs, Session, reactive, ui, render, module
from funciones.nav_panel_User import create_nav_menu_user
from clases.class_user_proyectName import global_user_proyecto
from api import *
from clases.global_session import global_session
from clases.global_sessionV2 import *
from funciones.funciones_user import create_modal_versiones, show_selected_project_card, create_modal_eliminar_bd, create_modal_v2, button_remove_version
from funciones.utils_2 import *
from logica_users.utils.help_versios import obtener_opciones_versiones, obtener_ultimo_id_version, eliminar_carpeta, mapear_valor_a_clave
from funciones.utils_cargar_json import leer_control_json
from api.db.sqlite_utils import *
from auth.utils import help_api 
from api.db.sqlite_utils import *
from funciones_modelo.global_estados_model import global_session_modelos
from funciones_modelo import help_models 




def versiones_config_server(input: Inputs, output: Outputs, session: Session,):
    #global_names_reactivos.name_validacion_in_sample_set(name_suffix)
    base_datos = 'Modeling_App.db'
    opciones_param = reactive.Value()
    valor_predeterminado_parms =  reactive.Value()
    versiones_por_proyecto = reactive.Value(None)
    
    
    
    


    @reactive.effect
    @reactive.event(input.other_select)  # Escuchar cambios en el selector
    def project_card_container():
        global_session.set_id_version(input.other_select()) # Captura el ID seleccionado
        global_session.id_version_v2.set(input.other_select())
        print("cuando entro a version???")
        nombre_version = obtener_nombre_version_por_id(global_session.get_id_version())
        
       
        files_name = get_records(
        table='name_files',
        columns=['id_files', 'nombre_archivo', 'fecha_de_carga'],
        join_clause='INNER JOIN version ON name_files.version_id = version.version_id',
        where_clause='version.version_id = ?',
        where_params=(global_session.get_id_version(),)
    )
        
        global_session_V2.lista_nombre_archivos_por_version.set({
            str(file['id_files']): file['nombre_archivo']
            for file in files_name
        } if files_name else {"": "No hay archivos"})

       
        #data = leer_dataset(global_session.get_id_user(), global_session.get_id_proyecto(), global_session.get_name_proyecto(), global_session_V2.lista_nombre_archivos_por_version.get(), global_session.get_versiones_name(), global_session.get_id_version())
        #global_session.set_data_set_reactivo(data)
        
        ult_model = obtener_ultimo_modelo_por_version_y_nombre(base_datos, global_session.get_id_version(), "desarollo")
      
        estado_model_desarrollo = help_models.obtener_estado_por_modelo(ult_model, "desarollo")
        
        global_session_modelos.modelo_desarrollo_estado.set(estado_model_desarrollo)
        
        fecha_model_desarrollo = help_models.obtener_fecha_por_modelo(ult_model, "desarollo")
       
        global_session_modelos.modelo_desarrollo_hora.set(fecha_model_desarrollo)
        
        print(global_session.get_version_parametros_id(), "viendo el maldito ID")
        estado_in_sample , hora_in_sample = help_models.procesar_etapa_in_sample_2(base_datos="Modeling_App.db", json_version_id=global_session.get_version_parametros_id(), etapa_nombre="in_sample")
        
        
        global_session_modelos.modelo_in_sample_estado.set(estado_in_sample)
        print(estado_in_sample, "estado in")
        global_session_modelos.modelo_in_sample_hora.set(hora_in_sample)
        print(hora_in_sample, "hora_in")
        
       
        
        ##ACTUALIZO EL ULTIMO SELECCIONADO EN LA TABALA DE BD
        actualizar_ultimo_seleccionado(base_datos, 'version', 'version_id', global_session.get_id_version())
        global_session.set_versiones_name(nombre_version)
        param_json = leer_control_json(global_session.get_id_user(), global_session.get_id_proyecto(), global_session.get_name_proyecto(), global_session.get_id_version(), global_session.get_versiones_name())
        global_session_V2.set_json_params_desarrollo(param_json)
        
        
        ##ACTUALIZO LAS VERSIONES DE NIELES Y SCORCARDS ACA Y EN LA SCREEN CORRESPONDIENTE DE NIVELES Y SC
        versiones_parametros = get_project_versions_param_mejorada(global_session.get_id_proyecto(), global_session.get_id_version())
        opciones_param.set(obtener_opciones_versiones(versiones_parametros, "id_jsons", "nombre_version")) 
        valor_predeterminado_parms.set(obtener_ultimo_id_version(versiones_parametros, "id_jsons"))
        
        selected_key = mapear_valor_a_clave(global_session_V2.get_dataSet_seleccionado(), global_session_V2.lista_nombre_archivos_por_version.get())
        
        ui.update_select("files_select", choices=global_session_V2.lista_nombre_archivos_por_version.get(),  selected=selected_key if selected_key else next(iter(global_session_V2.lista_nombre_archivos_por_version.get()), ""))
        ui.update_select("version_selector",choices=opciones_param.get(), selected=valor_predeterminado_parms.get())
    

    @output
    @render.ui
    def button_remove_versions():
            return button_remove_version(global_session.get_id_proyecto(), global_session.get_id_version())

    
    @reactive.Effect
    def boton_para_eliminar_version():
        eliminar_version_id = f"eliminar_version_{global_session.get_id_version()}"
        @reactive.Effect
        @reactive.event(input[eliminar_version_id])
        def eliminar_version_id():
            nombre_version = obtener_nombre_version_por_id(global_session.get_id_version())
            create_modal_v2(f"Seguro que quieres eliminar la version {nombre_version}?", "Confirmar", "Cancelar", "confirmar_eliminar_version", "cancelar_id")
            

    @reactive.Effect
    @reactive.event(input["confirmar_eliminar_version"])
    def eliminar_version_proyecto():
        
        eliminar_version("version", "version_id", global_session.get_id_version())
        path_carpeta_versiones_borrar_salida  = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}'
        path_carpeta_versiones_borrar_entrada  = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_entrada_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}'
        
        eliminar_carpeta(path_carpeta_versiones_borrar_salida)
        eliminar_carpeta(path_carpeta_versiones_borrar_entrada)
        columnas = ['version_id', 'nombre_version', 'execution_date']
        columnas = ["version_id", "project_id", "nombre_version", "execution_date", "is_last_selected"]
        tabla = "version"
        condiciones = "project_id = ?"
        parametros = (global_session.get_id_proyecto(),)  # project_id = 101

        # Llamar a la función con condiciones
        lista_de_versiones_new = obtener_versiones_por_proyecto(columnas, tabla, condiciones, parametros)

        #lista_de_versiones_new = obtener_versiones_por_proyecto(columnas, "version", global_session.get_id_proyecto(), "version", "project_id")

        versiones_por_proyecto.set(lista_de_versiones_new)
        ui.update_select(
            "other_select",
            choices={str(vers['version_id']): vers['nombre_version']
                     for vers in lista_de_versiones_new}
        )
        return ui.modal_remove()
        
    @reactive.Effect
    @reactive.event(input["cancelar_id"])
    def cancelar_eliminacion_version():
        return ui.modal_remove()
    