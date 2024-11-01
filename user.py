from shiny import App, Inputs, Outputs, Session, reactive, ui, render, module
from funciones.nav_panel_User import create_nav_menu_user
from clases.class_user_proyectName import global_user_proyecto
from api import *
from clases.global_session import global_session
from api.db import init_bd
import re
from funciones.funciones_user import create_project_selector, show_selected_project_card



def user_server(input: Inputs, output: Outputs, session: Session, name_suffix):
    user_get = reactive.Value(None)
    proyect_id = reactive.Value(None)
    proyect_ok = reactive.Value(False)
    #sanitized_name = re.sub(r'\W|^(?=\d)', '_', input['proyecto_nombre']())
    proyectos_usuario = reactive.Value(None)
    
    
        # Crear un reactive value para almacenar la lista de proyectos
    
    
    

   
    
   
    def see_session():
        @reactive.effect
        def enviar_session():
            if global_session.proceso.get():
                state = global_session.session_state.get()
                if state["is_logged_in"]:
                    user_id = state["id"]
                    proyectos_usuario.set(get_user_projects(user_id))#-> llamo a el valor reactivo para tener la lista de los proyectos por user, dinamicamente, apretar control t y ver la funcion
                    user_get.set(user_id.replace('|', '_'))
                    
    
    see_session()
    

    @reactive.effect
    @reactive.event(input.project_select)  # Escuchar cambios en el selector
    def project_card_container():
        selected_project_id = input.project_select()  # Captura el ID seleccionado
        global_session.set_id_proyect(selected_project_id)
        nombre_proyecto = obtener_nombre_proyecto_por_id(global_session.get_id_proyecto())
        global_session.proyecto_seleccionado.set(nombre_proyecto)
       

    @output
    @render.ui
    def project_card_container():
        if proyect_ok:
            return show_selected_project_card(user_get.get(),  global_session.get_id_proyecto())
        
    
   
    
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
                proyectos_usuario.set(get_user_projects(user))
                print(proyectos_usuario.get())
               
                # Actualiza la UI para mostrar el nuevo proyecto
                #ui.insert_ui(
                    #selector="#module_container",  # Cambia esto al selector adecuado donde quieras insertar
                    #where="afterEnd",  # O "beforeEnd" 0 afterBegin, según tu diseño
                    #ui=show_selected_project_card(user, proyect_id.get())  
                #)
                #update_project_list_ui(proyecto_por_user)
                create_navigation_handler('continuar', 'Screen_Desarollo')
                # Restablecer el estado a False
                global_user_proyecto.click_en_continuar.set(False)

    @output
    @render.ui
    def devolver_acordeon():
        projects = proyectos_usuario.get()  # Obtiene la lista actual de proyectos

        if projects:
            project_options = {str(project['id']): project['name'] for project in projects}
            return ui.div(
                ui.input_select(
                    "project_select",
                    "Selecciona un proyecto:",
                    project_options
                ),
                ui.output_ui("project_card_container")  # Contenedor para la tarjeta del proyecto
            )
        else:
            return ui.div("No hay proyectos disponibles para este usuario.")
    
    
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
