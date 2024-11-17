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
from funciones.help_versios import obtener_opciones_versiones, obtener_ultimo_id_version



def in_sample_verions(input: Inputs, output: Outputs, session: Session):
    
    list = reactive.Value(None)
    id_versiones_params = reactive.Value(None)
    opciones_param = reactive.Value(None)
    valor_predeterminado_parms = reactive.Value(None)
    

    @reactive.effect
    @reactive.event(input.create_parameters)
    def modal():
        return create_modal_versiones_param(global_session.get_name_proyecto(), global_session.get_versiones_name())

    @reactive.effect
    @reactive.event(input.continuar_version_param)
    def ok_verions():
        name = input['name_version_param']()
        print(name)
        add = add_param_versions(
        global_session.get_id_proyecto(), global_session.get_id_version(), name)
        global_session.set_version_parametros_id(add)
        id_versiones_params.set(add)
        print(add, "")
        crear_carpeta_version_parametros(global_session.get_id_user(), global_session.get_id_proyecto(), global_session.get_id_version(), global_session.get_version_parametros_id(), name, global_session.get_name_proyecto(), global_session.get_versiones_name())
        ##ACTUALIZO ACA TAMBIEN EL SELECTOR YA QUE SI LO HAGO ACA CUANDO PONEN CONTINUAR LE DA LA ULT VERSION
        versiones_parametros = get_project_versions_param(global_session.get_id_proyecto())
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
        versiones = get_project_versions_param(global_session.get_id_proyecto())
        
        
        
    @output
    @render.ui
    def button_remove_versions_param():
        versions_list = get_project_versions_param(global_session.get_id_proyecto())
        return button_remove(versions_list, id_versiones_params.get(), "id_jsons")
        
     
        
