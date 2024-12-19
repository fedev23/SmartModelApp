from clases.class_modelo import ModeloProceso
from shiny import reactive, render, ui
from clases.global_name import global_name_manager
from clases.global_modelo import global_desarollo
from funciones.create_menu_resul_model import create_nav_menu_result_model
from funciones.utils import retornar_card
from clases.class_user_proyectName import global_user_proyecto
from clases.global_modelo import modelo_of_sample
from clases.global_modelo import modelo_in_sample
from clases.global_session import global_session
from funciones.utils_2 import get_user_directory
from api.db import *
from clases.class_validacion import Validator

def server_modelos(input, output, session, name_suffix):
    mensaje = reactive.Value("")
    
    def see_session():
        @reactive.effect
        def enviar_session():
            if global_session.proceso.get():
                state = global_session.session_state.get()
                if state["is_logged_in"]:
                    user_id = state["id"]
                    user = get_user_directory(user_id)
                    print(user)
                    user_id_cleaned = user_id.replace('|', '_')
                    #directorio_desarollo.set(user)
                    #modelo_in_sample.script_path = f"./Validar_Desa.sh datos_entrada_{user_id_cleaned} datos_salida_{user_id_cleaned}"
    
    
    see_session()
    
    
 
    @output
    @render.text
    def nombre_proyecto_modelo():
        
        return f'Proyecto: {global_user_proyecto.mostrar_nombre_proyecto_como_titulo(global_session.proyecto_seleccionado())}'
    
   
    
    @output
    @render.ui
    def menu_modelo():
     return create_nav_menu_result_model(name_suffix)
    
    def create_navigation_handler(input_id, screen_name):
        @reactive.Effect
        @reactive.event(input[input_id])
        async def navigate():
            await session.send_custom_message('navigate', screen_name)
            
    
    
    create_navigation_handler("volver_etapas","Screen_User")
    
    
    
    ##FUNCION PARA RETORNAR LA TARJETA
   
    @output
    @render.text
    def mensaje_id_in_sample():
        return modelo_in_sample.mostrar_mensaje()
 
        
        
    @reactive.Effect
    @reactive.event(input[f'open_html_{modelo_in_sample.nombre}'])
    def enviar_result():
        ui.update_navs("Resultados_nav", selected="in_sample")
        create_navigation_handler(f'open_html_{modelo_in_sample.nombre}', 'Screen_Resultados')
        
        
    
      ##Retorna la tarjeta del accordeon Y modelo_out_to_sample
    
 
    @output
    @render.text
    def mensaje_of_sample():
        return modelo_of_sample.mostrar_mensaje()
 
        
        
    ##las demas instancias estan el cada servidor por un tema de prueba, luego vere si las dejo ahi o si las traigo aca