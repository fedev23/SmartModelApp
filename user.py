from shiny import App, Inputs, Outputs, Session, reactive, ui, render
from funciones.nav_panel_User import create_nav_menu_user
from clases.class_user_proyectName import global_user_proyecto
from api import *
from clases.global_session import global_session
from api.db import init_bd


def user_server(input: Inputs, output: Outputs, session: Session, name_suffix):
    user_get = reactive.Value(None)
    
    
    def see_session():
        @reactive.effect
        def enviar_session():
            if global_session.proceso.get():
                state = global_session.session_state.get()
                if state["is_logged_in"]:
                    user_id = state["id"]
                    user_get.set(user_id.replace('|', '_'))
                    
    
    see_session()
    
    @output
    @render.ui
    def nombre_proyecto_user():
        return ui.div()

    @output
    @render.ui
    def create_user_menu():
        return create_nav_menu_user(name_suffix)

    @reactive.effect
    @reactive.event(input[f'start_{name_suffix}'])
    def _():
        global_user_proyecto.create_modal()
        global_user_proyecto.cancelar_buton(input)
        global_user_proyecto.continuar_buton(input)
        # global_user_proyecto.click_en_continuar.set(True)

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
                #init_bd.list_tables()
                add_project(user, name)
                print("llegue hasta aca?")
                proyecto_por_user = get_user_projects(user)
                print(proyecto_por_user)
                create_navigation_handler('continuar', 'Screen_Desarollo')
                # Restablecer el estado a False
                global_user_proyecto.click_en_continuar.set(False)

    @output
    @render.ui
    def devolver_acordeon():
        return global_user_proyecto.create_accordeon(user_get.get())
    
    
    @reactive.effect
    @reactive.event(input[f'settings_{name_suffix}'])
    async def log_out():
        create_navigation_handler('settings_user', 'Screen_Login')
        await session.close()
        
        
    
    @reactive.effect
    @reactive.event(input.close)
    async def _():
        await session.close()
      

    

    def create_navigation_handler(input_id, screen_name):
        @reactive.Effect
        @reactive.event(input[input_id])
        async def navigate():
            await session.send_custom_message('navigate', screen_name)

    # create_navigation_handler('finalizar', 'Screen_Desarollo')

    create_navigation_handler('load_Validacion_user', 'Screen_valid')
    create_navigation_handler('load_Validacion_user', 'Screen_valid')
    create_navigation_handler('screen_Desarollo_user', 'Screen_Desarollo')
    create_navigation_handler('screen_Produccion_user', 'Screen_Porduccion')
    create_navigation_handler('ir_result_user', 'Screen_Resultados')
    create_navigation_handler('ir_carga_user', 'Screen_Desarollo')
    create_navigation_handler('ir_modelos_user', 'Screen_3')
    create_navigation_handler('screen_in_sample_user', 'screen_in_sample')

    @reactive.Effect
    @reactive.event(input.ir_carga_archivos)
    async def go_to_carga_load_fila():
        await session.send_custom_message('navigate', 'Screen_Desarollo')
