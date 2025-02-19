from shiny import App, Inputs, Outputs, Session, reactive, ui, render, module
from clases.reactives_name import *
from api import *
from funciones.help_parametros.valid_columns import replace_spaces_with_underscores
from clases.global_session import global_session
from clases.global_sessionV2 import *
from funciones.funciones_user import create_modal_v2, button_remove_version
from funciones.utils_2 import *
from clases.global_sessionV3 import *
from clases.global_modelo import global_desarollo
from logica_users.utils.help_versios import obtener_opciones_versiones, obtener_ultimo_id_version, eliminar_carpeta, mapear_valor_a_clave
from funciones.utils_cargar_json import leer_control_json
from api.db.sqlite_utils import *
from funciones_modelo.help_models import *
from funciones_modelo.warning_model import tiene_modelo_ejecutado, obtener_nombre_dataset, verificar_estado_modelo
from api.db.sqlite_utils import *
from funciones_modelo.global_estados_model import global_session_modelos
from funciones_modelo import help_models 
from logica_users.utils.manejo_session import manejo_de_ultimo_seleccionado



def versiones_config_server(input: Inputs, output: Outputs, session: Session,):
    #global_names_reactivos.name_validacion_in_sample_set(name_suffix)
    base_datos = 'Modeling_App.db'
    opciones_param = reactive.Value()
    valor_predeterminado_parms =  reactive.Value()
    versiones_por_proyecto = reactive.Value(None)
    init_session = reactive.Value(True)
    ultimo_id_version_reactivo = reactive.Value()

    
    
    
    


    @reactive.effect
    @reactive.event(input.other_select)  # Escuchar cambios en el selector
    def project_card_container():
        id_version  = input.other_select() # Captura el ID seleccionado
        ultimo_id = obtener_ultimo_id_seleccionado(base_datos, "version", "version_id"),
        if isinstance(ultimo_id, tuple):
                ultimo_id_version_reactivo.set(ultimo_id[0])  #
        
        manejo_de_ultimo_seleccionado(
        is_initializing=init_session,
        input_select_value=input.other_select(),
        ultimo_id_func=lambda: obtener_ultimo_id_seleccionado(base_datos, "version", "version_id"),
        global_set_func=lambda x: global_session.set_id_version(x),
        actualizar_ultimo_func=lambda table, column, value: actualizar_ultimo_seleccionado(base_datos, table, column, value),
        obtener_ultimo_func=lambda table, column: obtener_ultimo_seleccionado(base_datos, table, column),
        obtener_opciones_func=lambda: obtener_opciones_versiones(get_project_versions(global_session.get_id_proyecto()), "version_id", "nombre_version"),
        mapear_clave_func=mapear_valor_a_clave,
        ui_update_func=lambda name, choices, selected: ui.update_select(name, choices=choices, selected=selected),
        input_select_name="other_select",
        db_table="version",
        db_column_id="version_id",
        db_column_name="nombre_version"
    )

        
        model_ok = verificar_estado_modelo(base_datos, version_id=global_session.get_id_version(), dataset_id=global_session.get_id_dataSet())
        if model_ok:
            nombre_dataSet_con_modelo = obtener_nombre_dataset(global_session.get_id_version())
            global_names_reactivos.set_name_file_db(nombre_dataSet_con_modelo)
        
        
        nombre_version = obtener_nombre_version_por_id(global_session.get_id_version())
        
        files_name = get_records(
        table='name_files',
        columns=['id_files', 'nombre_archivo', 'fecha_de_carga'],
        where_clause='project_id = ?',  # Cambiar la cláusula a usar project_id directamente
        where_params=(global_session.get_id_proyecto(),)
    )
        
        global_session_V2.lista_nombre_archivos_por_version.set({
            str(file['id_files']): file['nombre_archivo']
            for file in files_name
        } if files_name else {"": "No hay archivos"})
        
        ##VALIDA LA EXISTENCIA DEL MODELO, SI ESE MODELO TIENE UNA VERSION CON UN NOMBRE DEL DATASET ASOCIADO CARGA ESE
        modelo_existente = tiene_modelo_ejecutado(db_path=base_datos, version_id=global_session.get_id_version())
            
        if  modelo_existente:
            nombre_dataSet_con_modelo = obtener_nombre_dataset(global_session.get_id_version())
            global_session_V2.set_dataSet_seleccionado(nombre_dataSet_con_modelo)
            selected_key = mapear_valor_a_clave(global_session_V2.get_dataSet_seleccionado(), global_session_V2.lista_nombre_archivos_por_version.get())
            ui.update_select("files_select", choices=global_session_V2.lista_nombre_archivos_por_version.get(),  selected=selected_key if selected_key else next(iter(global_session_V2.lista_nombre_archivos_por_version.get()), ""))
        else:
            ultimo_archivo = obtener_ultimo_seleccionado(base_datos, 'name_files', 'nombre_archivo')
            global_session_V2.set_dataSet_seleccionado(ultimo_archivo)
            selected_key = mapear_valor_a_clave(global_session_V2.get_dataSet_seleccionado(), global_session_V2.lista_nombre_archivos_por_version.get())
            ui.update_select("files_select", choices=global_session_V2.lista_nombre_archivos_por_version.get(),  selected=selected_key if selected_key else next(iter(global_session_V2.lista_nombre_archivos_por_version.get()), ""))
            
           
        #CAPTURO ESTADO DEL MODELO DE  DESARROLLO
        estado_model_desarrollo, fecha_model_desarrollo, mensaje_errro = help_models.procesar_etapa(base_datos="Modeling_App.db", id_version=global_session.get_id_version(), etapa_nombre=global_desarollo.nombre)
        
        global_session_modelos.modelo_desarrollo_estado.set(estado_model_desarrollo)
        global_session_modelos.modelo_desarrollo_hora.set(fecha_model_desarrollo)
        global_session_modelos.modelo_desarrollo_mensaje_error.set(mensaje_errro)
        
        #CAPTURO EL ESTADO DEL MODELO IN SAMPLE
        estado_in_sample , hora_in_sample, mensaje_error = help_models.procesar_etapa_in_sample_2(base_datos="Modeling_App.db", json_version_id=global_session.get_version_parametros_id(), etapa_nombre="in_sample")
        global_session_modelos.modelo_in_sample_estado.set(estado_in_sample)
        global_session_modelos.modelo_in_sample_hora.set(hora_in_sample)
        global_session_modelos.modelo_in_sample_mensaje_error.set(mensaje_error)
    

            
        ##ACTUALIZO EL ULTIMO SELECCIONADO EN LA TABALA DE BD
        #actualizar_ultimo_seleccionado(base_datos, 'version', 'version_id', global_session.get_id_version())
        global_session_V3.name_version_original.set(nombre_version)
        global_session.set_versiones_name(replace_spaces_with_underscores(nombre_version))
        
        param_json = leer_control_json(global_session.get_id_user(), global_session.get_id_proyecto(), global_session.get_name_proyecto(), global_session.get_id_version(), global_session.get_versiones_name())
        global_session_V2.set_json_params_desarrollo(param_json)
        
        
        

    @output
    @render.ui
    def button_remove_versions():
            return button_remove_version(global_session.get_id_proyecto(), global_session.get_id_version())

    
    delete_button_effects = {}  # Diccionario para rastrear los efectos ya definidos

    @reactive.Effect
    def boton_para_eliminar_version():
        eliminar_version_id = f"eliminar_version_{global_session.get_id_version()}"

        # Verificar si ya existe un manejador para este botón
        if eliminar_version_id not in delete_button_effects:
            print("Creando efecto para:", eliminar_version_id)

            # Definir el efecto para el botón específico
            def eliminar_version_boton():
                nombre_version = obtener_nombre_version_por_id(global_session.get_id_version())
                print(f"Botón {eliminar_version_id} activado para eliminar la versión {nombre_version}.")
                create_modal_v2(
                    f"¿Seguro que quieres eliminar la versión {nombre_version}?",
                    "Confirmar",
                    "Cancelar",
                    "confirmar_eliminar_version",
                    "cancelar_id"
                )

            # Asociar el evento al botón
            @reactive.effect
            @reactive.event(input[eliminar_version_id])
            def manejar_eliminar_boton():
                eliminar_version_boton()

            # Registrar el efecto en el diccionario
            delete_button_effects[eliminar_version_id] = manejar_eliminar_boton
        else:
            print("Efecto ya definido para:", eliminar_version_id)

    @reactive.Effect
    @reactive.event(input["confirmar_eliminar_version"])
    def eliminar_version_proyecto():
        
        eliminar_version("version", "version_id", global_session.get_id_version())
        
        nombre_version_sin_espacios = replace_spaces_with_underscores(global_session.get_versiones_name())
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
    
    
    
    @reactive.effect
    def update_nav():
        id_actual = input.other_select()
        if id_actual != "a" and id_actual != "":
            id_actual = int(id_actual)
            
            print(f"id_actual {id_actual}")
            print(f"ultimo_id_version_reactivo.get() {ultimo_id_version_reactivo.get()}")
            if ultimo_id_version_reactivo.get() != id_actual:
                ##ACTUALIZO LAS VERSIONES DE NIELES Y SCORCARDS ACA Y EN LA SCREEN CORRESPONDIENTE DE NIVELES Y SC
                versiones_parametros = get_project_versions_param_mejorada(global_session.get_id_proyecto(), global_session.get_id_version())
                opciones_param.set(obtener_opciones_versiones(versiones_parametros, "id_jsons", "nombre_version")) 
                valor_predeterminado_parms.set(obtener_ultimo_id_seleccionado_edited(base_datos, "json_versions", "id_jsons", global_session.get_id_version()))
                print(valor_predeterminado_parms.get(), "valuee??")
                print(opciones_param.get())
                ##VIRFICIAR SI ESTO ESTA BIEN, QUE SOLO SE HAGA UN UPDATE EN IN SMAPELVERSIONS.
                ui.update_select("version_selector",choices=opciones_param.get(), selected=valor_predeterminado_parms.get())
            
                ui.update_navs("navset", selected="screen_desarrolo")  # Cambia al panel deseado
                global_session_V2.click_seleccion_niveles_score.set(0)
