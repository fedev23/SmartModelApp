#create_parameters

from shiny import App, Inputs, Outputs, Session, reactive, ui, render, module
from funciones.nav_panel_User import create_nav_menu_user
from clases.class_user_proyectName import global_user_proyecto
from api import *
from clases.global_session import global_session
from clases.global_reactives import global_estados
from funciones.funciones_user import  create_modal_v2, create_modal_versiones_param
from api.db import *
from funciones.utils_2 import crear_carpeta_version_parametros

def in_sample_verions(input: Inputs, output: Outputs, session: Session):
    
    @reactive.effect
    @reactive.event(input.create_parameters)
    def modal():
        return  create_modal_versiones_param(global_session.get_name_proyecto(), global_session.get_versiones_name())
    
    @reactive.effect
    @reactive.event(input.continuar_version_param)
    def ok_verions():
      name = input['name_version_param']()
      print(name)
      add = add_param_versions(global_session.get_id_proyecto(), global_session.get_id_version(), name)
      global_session.set_version_parametros_id(add)
      add =crear_carpeta_version_parametros(global_session.get_id_user(), global_session.get_id_proyecto(), global_session.get_id_version(), global_session.get_version_parametros_id(), name, global_session.get_name_proyecto(), global_session.get_versiones_name())
      print(add)
      ui.modal_remove()
 
    @reactive.effect
    @reactive.event(input.cancelar_version_param)
    def Ko_verions():
      ui.modal_remove()
    
    
    


