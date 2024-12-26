from shiny import App, Inputs, Outputs, Session, reactive, ui, render, module
from funciones.nav_panel_User import create_nav_menu_user
from clases.class_user_proyectName import global_user_proyecto
from api import *
from clases.global_session import global_session
from clases.global_sessionV2 import *
from funciones.funciones_user import create_modal_versiones, show_selected_project_card, create_modal_eliminar_bd, create_modal_v2, button_remove_version
from funciones.utils_2 import crear_carpeta_proyecto, crear_carpeta_version_por_proyecto, get_datasets_directory
from logica_users.utils.help_versios import obtener_opciones_versiones, obtener_ultimo_id_version, eliminar_carpeta, mapear_valor_a_clave
from funciones.utils_cargar_json import leer_control_json
from api.db.sqlite_utils import *
from auth.utils import help_api 
from api.db.sqlite_utils import *
from funciones_modelo.global_estados_model import global_session_modelos
from funciones_modelo import help_models 

def user_server(input: Inputs, output: Outputs, session: Session, name_suffix):
    user_get = reactive.Value(None)
    proyect_ok = reactive.Value(False)
    proyectos_usuario = reactive.Value(None)
    proceso_eliminar = reactive.Value(False)
    versiones_por_proyecto = reactive.Value(None)
    nombre_file = reactive.Value(None)
    id_proyecto_Recien_Creado = reactive.Value(None)
    name_proyecto = reactive.Value(None)
    opciones_param = reactive.Value("")
    opciones_de_versiones_por_proyecto = reactive.Value("")
    ultimo_proyecto_seleccionado =  reactive.Value("")
    ultimo_id_versiones_proyecto = reactive.Value("")
    valor_predeterminado_parms = reactive.Value("")
    boolean_check = reactive.Value(False)
    data_predeterminado = reactive.Value("")
    base_datos = 'Modeling_App.db'
    
    def see_session():
        @reactive.effect
        def enviar_session():
            if global_session.proceso.get():
                state = global_session.session_state.get()
                if state["is_logged_in"]:
                    user_id = state["id"]
                    global_session.id_user.set(user_id)
                    # -> llamo a el valor reactivo para tener la lista de los proyectos por user, dinamicamente, apretar control t y ver la funcion
                    global_session.set_proyectos_usuarios(get_user_projects(user_id))
                    user_get.set(user_id.replace('|', '_'))
                    proyectos_usuario.set(get_user_projects(global_session.get_id_user()))
        
                    #ui.update_select("project_select",choices=proyectos_choise, selected=key_proyecto_mach if key_proyecto_mach else next(iter(proyectos_choise), ""))
        
                    

    see_session()

    

    @reactive.effect
    @reactive.event(input.project_select)  # Escuchar cambios en el selector
    def project_card_container():
        # Captura el ID del proyecto seleccionado
        selected_project_id = input.project_select()
        #print(selected_project_id, "proyecto")
        global_session.set_id_proyect(selected_project_id)

        nombre_proyecto = obtener_nombre_proyecto_por_id(global_session.get_id_proyecto())
        global_session.set_name_proyecto(nombre_proyecto)
        
        actualizar_ultimo_seleccionado(base_datos, 'project', 'id', global_session.get_id_proyecto())
        proyectos_usuario.set(get_user_projects(global_session.get_id_user()))
        
        proyectos_choise = obtener_opciones_versiones(proyectos_usuario.get(), "id", "name")
       
        ultimo_proyecto_seleccionado.set(obtener_ultimo_seleccionado(base_datos, 'project', 'name'))
       
        key_proyecto_mach = mapear_valor_a_clave(ultimo_proyecto_seleccionado.get(), proyectos_choise)
        
        versiones_de_proyecto = get_project_versions(global_session.get_id_proyecto())
        opciones_de_versiones_por_proyecto.set(obtener_opciones_versiones(versiones_de_proyecto, "version_id", "nombre_version"))
        
        ultimo_id_versiones_proyecto.set(obtener_ultimo_seleccionado(base_datos, 'version', 'nombre_version'))

        key_versiones_mach = mapear_valor_a_clave(ultimo_id_versiones_proyecto.get(), opciones_de_versiones_por_proyecto.get())
        # Si hay versiones, establece el nombre de la primera versión como predeterminado
        if boolean_check():
            nombre_version = obtener_nombre_version_por_id(global_session.get_id_version())
            global_session.set_versiones_name(nombre_version)
            

        # Obtiene los archivos relacionados con el proyecto
        files_name = get_records(
        table='name_files',
        columns=[
            'id_files', 
            'nombre_archivo', 
            'fecha_de_carga'
        ],
        join_clause='INNER JOIN version ON name_files.version_id = version.version_id',
        where_clause='version.project_id = ?',
        where_params=(global_session.get_id_proyecto(),)
    )
        
    
        nombre_file.set({
            str(file['id_files']): file['nombre_archivo']
            for file in files_name
        } if files_name else {"": "No hay archivos"})

        # Obtiene y configura las versiones de parámetros
        versiones_parametros  = get_project_versions_param(global_session.get_id_proyecto(), global_session.get_id_version())
            # 
        #versiones_parametros = get_project_versions_param_mejorada(global_session.get_id_proyecto(), global_session.get_id_version()
        
        opciones_param.set(obtener_opciones_versiones(versiones_parametros, "id_jsons", "nombre_version"))
        valor_predeterminado_parms.set(obtener_ultimo_id_version(versiones_parametros, "id_jsons"))

        # Crea el path para guardar datasets
        data_Set = crear_carpeta_proyecto(user_get.get(), global_session.get_id_proyecto(), global_session.get_name_proyecto())
        global_session.set_path_guardar_dataSet_en_proyectos(data_Set)
        
        
        ##Actualizo tambien los dataSet de Validacion y scroing
        nombre_files_validacion_sc = get_records(
            table='validation_scoring',
            columns=['id_validacion_sc', 
                    'nombre_archivo_validation_sc', 
                    'fecha_de_carga'],
            join_clause='INNER JOIN version ON validation_scoring.version_id = version.version_id',
            where_clause='version.project_id = ?',
            where_params=(global_session.get_id_proyecto(),)
        )
        
        global_session_V2.set_opciones_name_dataset_Validation_sc(obtener_opciones_versiones(nombre_files_validacion_sc, "id_validacion_sc", "nombre_archivo_validation_sc"))
        data_predeterminado.set(obtener_ultimo_id_version(nombre_files_validacion_sc, 'id_validacion_sc'))

        #LEEO ELDATA SET SI EXISTE
        # Actualiza los selectores en la UI
        nombre_version = obtener_nombre_version_por_id(global_session.get_id_version())
        global_session.set_versiones_name(nombre_version)

        if (global_session.get_id_user() and
            global_session.get_name_proyecto() and
            global_session.get_id_proyecto() and
            global_session.get_id_version() and
            global_session.get_versiones_name()):   
            help_api.procesar_starlette_api(global_session.get_id_user(), global_session.get_name_proyecto(), global_session.get_id_proyecto(), global_session.get_id_version(), global_session.get_versiones_name())
        
        
        ultimo_archivo = obtener_ultimo_seleccionado(base_datos, 'name_files', 'nombre_archivo')
        global_session_V2.set_dataSet_seleccionado(ultimo_archivo)
        selected_key = mapear_valor_a_clave(global_session_V2.get_dataSet_seleccionado(), nombre_file.get())
        
        
        ui.update_select("project_select",choices=proyectos_choise, selected=key_proyecto_mach if key_proyecto_mach else next(iter(ultimo_proyecto_seleccionado.get()), ""))
        ui.update_select("files_select_validation_scoring",choices=global_session_V2.get_opciones_name_dataset_Validation_sc(), selected=data_predeterminado.get())
        ui.update_select("files_select", choices=nombre_file.get(),  selected=selected_key if selected_key else next(iter(nombre_file.get()), ""))
        ui.update_select("other_select", choices=opciones_de_versiones_por_proyecto.get(), selected=key_versiones_mach if key_versiones_mach else next(iter(opciones_de_versiones_por_proyecto.get()), ""))
        ui.update_select("version_selector", choices=opciones_param.get(), selected=valor_predeterminado_parms.get())

    @output
    @render.ui
    def project_card_container():
        if proyect_ok:
            return show_selected_project_card(user_get.get(),  global_session.get_id_proyecto())

    @reactive.effect
    @reactive.event(input.other_select)  # Escuchar cambios en el selector
    def project_card_container():
        global_session.set_id_version(input.other_select()) # Captura el ID seleccionado
        global_session.id_version_v2.set(input.other_select())
        nombre_version = obtener_nombre_version_por_id(global_session.get_id_version())
        
        print(global_session.get_id_version(), "en version")
        ult_model = obtener_ultimo_modelo_por_version_y_nombre(base_datos, global_session.get_id_version(), "desarollo")
      
        estado_model_desarrollo = help_models.obtener_estado_por_modelo(ult_model, "desarollo")
        
        global_session_modelos.modelo_desarrollo_estado.set(estado_model_desarrollo)
        
        fecha_model_desarrollo = help_models.obtener_fecha_por_modelo(ult_model, "desarollo")
       
        global_session_modelos.modelo_desarrollo_hora.set(fecha_model_desarrollo)
        
        ##ACTUALIZO EL ULTIMO SELECCIONADO EN LA TABALA DE BD
        actualizar_ultimo_seleccionado(base_datos, 'version', 'version_id', global_session.get_id_version())
        global_session.set_versiones_name(nombre_version)
        param_json = leer_control_json(global_session.get_id_user(), global_session.get_id_proyecto(), global_session.get_name_proyecto(), global_session.get_id_version(), global_session.get_versiones_name())
        global_session_V2.set_json_params_desarrollo(param_json)
        
        
        ##ACTUALIZO LAS VERSIONES DE NIELES Y SCORCARDS ACA Y EN LA SCREEN CORRESPONDIENTE DE NIVELES Y SC
        versiones_parametros = get_project_versions_param(global_session.get_id_proyecto(), global_session.get_id_version())
        opciones_param.set(obtener_opciones_versiones(versiones_parametros, "id_jsons", "nombre_version")) 
        valor_predeterminado_parms.set(obtener_ultimo_id_version(versiones_parametros, "id_jsons"))
        
        ui.update_select("version_selector",choices=opciones_param.get(), selected=valor_predeterminado_parms.get())
   
    @output
    @render.ui
    def button_remove_versions():
        if proyect_ok:
            return button_remove_version(global_session.get_id_proyecto(), global_session.get_id_version())

    # boton para eliminar proyecto

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
        ui.modal_remove()
        
    @reactive.Effect
    @reactive.event(input["cancelar_id"])
    def cancelar_eliminacion_version():
        return ui.modal_remove()
    
    @reactive.Effect
    @reactive.event(input["cancelar"])
    def cancelar_eliminacion_version():
        return ui.modal_remove()
    
    @reactive.Effect
    @reactive.event(input["cancelar_version"])
    def cancelar_eliminacion_version():
        return ui.modal_remove()
        
    @reactive.Effect
    @reactive.event(input["confirmar_id_dataset"])
    def eliminar_dataset():
        eliminar_version('name_files', 'id_files',global_session.get_id_dataSet())
        columnas = ['id_files', 'nombre_archivo', 'fecha_de_carga']
        lista_de_versiones_new = obtener_versiones_por_proyecto(
            global_session.get_id_proyecto(), columnas, "name_files", "project_id")
        nombre_file.set(lista_de_versiones_new)
        ui.update_select(
            "files_select",
            choices={str(vers['id_files']): vers['nombre_archivo']
                     for vers in lista_de_versiones_new}
        )
        ui.modal_remove()

    # boton para eliminar proyecto

    @reactive.Effect
    def handle_delete_buttons():
        project_id = global_session.get_id_proyecto()
        eliminar_btn_id = f"eliminar_proyect_{project_id}"

        @reactive.Effect
        @reactive.event(input[eliminar_btn_id])
        def eliminar_proyecto_boton():
            create_modal_eliminar_bd()

    @reactive.Effect
    @reactive.event(input["eliminar_proyecto_modal"])
    def eliminar_proyeco_modal():
        eliminar_proyecto(global_session.get_id_proyecto())
        # Actualiza proyectos_usuario después de eliminar el proyecto
        #proyectos_actualizados = get_user_projects(user_get.get())
        proyectos_actualizados = get_records(
            table='project',  # Nombre de la tabla
            columns=['id', 'name'],  # Columnas que deseas recuperar
            where_clause='user_id = ?',  # Cláusula WHERE
            where_params=(user_get.get(),)  # Parámetros para el filtro (reemplaza 123 por el user_id deseado)
        )
        # Refresca proyectos_usuario con la lista actualizada
        path_carpeta_versiones_borrar_salida  = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}'
        path_carpeta_versiones_borrar_entrada  = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_entrada_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}'
        
        eliminar_carpeta(path_carpeta_versiones_borrar_salida)
        eliminar_carpeta(path_carpeta_versiones_borrar_entrada)
        
        proyectos_usuario.set(proyectos_actualizados)
        ultimo_id_versiones_proyecto.set(obtener_ultimo_id_version(proyectos_actualizados, "id"))
        
        
        # Actualiza el selector con los proyectos restantes
        ui.update_select(
            "project_select",
            choices={str(proj['id']): proj['name']
                     for proj in proyectos_actualizados}
        )

        proceso_eliminar.set(True)
        ui.modal_remove()

        # return show_selected_project_card(user_get.get(),  global_session.get_id_proyecto())

    @reactive.Effect
    @reactive.event(input["cancelar_eliminar"])
    def canacelar_eliminacion():
        ui.modal_remove()

    @output
    @render.ui
    def nombre_proyecto_user():
        return ui.div()

    @output
    @render.ui
    def create_user_menu():
        return create_nav_menu_user(name_suffix)

    @reactive.effect
    @reactive.event(input[f'version_{name_suffix}'])
    def _():
        # print(id, "estoy en el supuesto id")
        nombre_proyecto = obtener_nombre_proyecto_por_id(
            global_session.get_id_proyecto())
        create_modal_versiones(nombre_proyecto)

    @reactive.effect
    @reactive.event(input.cancelar_eliminar)
    def cancel_version():
        ui.modal_remove()
        # agregar_version


    @reactive.effect
    @reactive.event(input.continuar_version)
    def agregar_ver():
        name = input[f'name_version']()
        id_proyect = global_session.get_id_proyecto()
        global_session.set_id_version(agregar_version(id_proyect, name))

        
        versiones = get_project_versions(global_session.get_id_proyecto())
        # actualizo la version por proyecto id
        opciones_de_versiones_por_proyecto.set(obtener_opciones_versiones(versiones, "version_id", "nombre_version"))
        ultimo_id_versiones_proyecto.set(obtener_ultimo_id_version(versiones, "version_id"))
        

        ui.update_select("other_select", choices=opciones_de_versiones_por_proyecto.get(), selected=ultimo_id_versiones_proyecto.get())
        global_session.set_proyecto_seleccionado_id(id_proyecto_Recien_Creado.get())
        print(global_session.get_id_version(), "ANTES DE CREAR UNA VERSION")
        crear_carpeta_version_por_proyecto(user_get.get(), global_session.get_id_proyecto(), ultimo_id_versiones_proyecto.get(), name, global_session.get_name_proyecto())
        ui.modal_remove()


    ##EVENTO PARA LA CREACION DEL PROYECTO
    @reactive.effect
    @reactive.event(input[f'start_{name_suffix}'])
    def crear_version():
        global_user_proyecto.create_modal()
        global_user_proyecto.cancelar_buton(input)
        global_user_proyecto.continuar_buton(input)

    @reactive.Effect
    @reactive.event(input.continuar)
    def finalizar_click():
        if global_user_proyecto.click_en_continuar.get() is False:
            # Solo procesa si `click_en_continuar` aún no ha sido activado
            global_user_proyecto.click_en_continuar.set(True)
            ui.modal_remove()

            # Verifica el estado actual antes de proceder
            if global_user_proyecto.click_en_continuar.get():
                user = user_get.get()
                name = input[f'proyecto_nombre']()
                
                # Crear el proyecto y obtener su ID
                global_session.set_name_proyecto(name)
                name_proyecto.set(name)
                global_session.set_id_proyect(add_project(user, name))  # Esta función debería establecer el ID del proyecto recién creado en la sesión global
                proyectos_usuario.set(get_user_projects(user))

                # Aquí asegúrate de que `add_project` o cualquier otro mecanismo te da el `project_id`
                proyect_id = global_session.get_id_proyecto()  # Obtener el ID del proyecto recién creado

                # Establecer el ID en el estado global para que lo puedan usar otros efectos
                id_proyecto_Recien_Creado.set(proyect_id)

                global_session.set_proyecto_seleccionado_id(id_proyecto_Recien_Creado.get())

                 
                # Actualiza el selector con los proyectos restantes
                ui.update_select("project_select", choices={str(proj['id']): proj['name'] for proj in get_user_projects(user_get.get())}
                )

                global_session.set_id_user(user_get())
                crear_carpeta_proyecto(user_get.get(), global_session.get_id_proyecto(), name)
                data_Set = get_datasets_directory(user_get.get(), global_session.get_id_proyecto(), global_session.get_name_proyecto())
                global_session.set_path_guardar_dataSet_en_proyectos(data_Set)

                # Reinicia el estado de click en continuar
                global_user_proyecto.click_en_continuar.set(False)

    
        

    @reactive.effect
    @reactive.event(input.close)
    async def _():
        await session.close()
