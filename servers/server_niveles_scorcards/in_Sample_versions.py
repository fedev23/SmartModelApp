# create_parameters

from shiny import App, Inputs, Outputs, Session, reactive, ui, render, module
from funciones.nav_panel_User import create_nav_menu_user
from clases.class_user_proyectName import global_user_proyecto
from api import *
from clases.global_session import global_session
from clases.global_reactives import global_estados
from funciones.funciones_user import create_modal_v2, create_modal_versiones_param, button_remove
from api.db import *
from funciones.utils_2 import crear_carpeta_version_parametros
from logica_users.utils.help_versios import obtener_opciones_versiones, obtener_ultimo_id_version
from datetime import datetime


def in_sample_verions(input: Inputs, output: Outputs, session: Session, name_para_button):
    
    list = reactive.Value(None)
    id_versiones_params = reactive.Value(None)
    opciones_param = reactive.Value(None)
    valor_predeterminado_parms = reactive.Value(None)
    nombre_version_seleccionador = reactive.Value(None)
    

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
        print(f"se me imprimio el id? {add}")
        global_session.set_version_parametros_id(add)
        id_versiones_params.set(add)
        
        nombre_version = obtener_nombre_version_por_id(global_session.get_id_version())
        crear_carpeta_version_parametros(global_session.get_id_user(), global_session.get_id_proyecto(), global_session.get_id_version(), global_session.get_version_parametros_id(), name, global_session.get_name_proyecto(), global_session.get_versiones_name())

        ##ACTUALIZO ACA TAMBIEN EL SELECTOR YA QUE SI LO HAGO ACA CUANDO PONEN CONTINUAR LE DA LA ULT VERSION
        versiones_parametros = get_project_versions_param(global_session.get_id_proyecto(), global_session.get_id_version())
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
        versiones_id = input.version_selector()
        id_versiones_params.set(versiones_id)
        global_session.set_version_parametros_id(id_versiones_params.get())
        versiones = get_project_versions_param(global_session.get_id_proyecto(), global_session.get_id_version())
        print(versiones, "QUE TIENE LA VERSIONES???")
        if versiones:
            if opciones_param.get() is  None:
                nombre_version = versiones[0]['nombre_version']
                print(nombre_version)
                global_session.set_versiones_parametros_nombre(obtener_valor_por_id_versiones(global_session.get_version_parametros_id()))
            
              
        
    @output
    @render.ui
    def button_remove_versions_param():
        versions_list = get_project_versions_param(global_session.get_id_proyecto(), global_session.get_id_version())
        name = global_session.get_versiones_name
        return button_remove(versions_list, id_versiones_params.get(), "id_jsons", name_para_button)
    
    
    @reactive.Effect
    def handle_delete_buttons():
        id_verisones_param = global_session.get_version_parametros_id()
        print(id_verisones_param, "estoy en versiones")
        eliminar_btn_id = f"eliminar_version_{global_session.get_version_parametros_id()}_{name_para_button}"
        @reactive.Effect
        @reactive.event(input[eliminar_btn_id])
        def eliminar_param_boton():
            print("pase")
            create_modal_v2("Eliminar versión de parametros", "Confirmar", "Cancelar", "confirmar_remove", "cancelar_remove")
        
        
    @reactive.Effect
    @reactive.event(input.confirmar_remove)
    def remove_versiones_de_parametros():
        eliminar_version("json_versions", "id_jsons", id_versiones_params.get())
        columnas = ['id_jsons', 'nombre_version']
        lista_de_versiones_new = obtener_versiones_por_proyecto(global_session.get_id_proyecto(), columnas, "json_versions", "project_id")
        print(lista_de_versiones_new)
        list.set(lista_de_versiones_new)
        ui.update_select(
            "version_selector",
            choices={str(vers['id_jsons']): vers['nombre_version']
                     for vers in lista_de_versiones_new}
        )
        ui.modal_remove()
    
    
    
        
    
        
     
        
