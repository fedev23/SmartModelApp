from shiny import App, Inputs, Outputs, Session, reactive, ui, render, module
from funciones.nav_panel_User import create_nav_menu_user
from clases.class_user_proyectName import global_user_proyecto
from api import *
from clases.global_session import global_session
from clases.global_reactives import global_estados
from funciones.funciones_user import create_project_selector, show_selected_project_card, create_modal_eliminar_bd



def user_server(input: Inputs, output: Outputs, session: Session, name_suffix):
    user_get = reactive.Value(None)
    proyect_ok = reactive.Value(False)
    proyectos_usuario = reactive.Value(None)
    proceso_eliminar = reactive.Value(False)

    
    def see_session():
        @reactive.effect
        def enviar_session():
            if global_session.proceso.get():
                state = global_session.session_state.get()
                if state["is_logged_in"]:
                    user_id = state["id"]
                    global_session.id_user.set(user_id)
                    proyectos_usuario.set(get_user_projects(user_id))#-> llamo a el valor reactivo para tener la lista de los proyectos por user, dinamicamente, apretar control t y ver la funcion
                    user_get.set(user_id.replace('|', '_'))
                    
    
    see_session()
    
    @reactive.effect
    def capturar_num_seleccionador_dataSet():
        select_number_data_set = input.number_choice()
        global_estados.set_numero_dataset(select_number_data_set)
        
    

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
        
    ##boton para eliminar proyecto
    @reactive.Effect
    def handle_delete_buttons():
        project_id = global_session.get_id_proyecto()
        eliminar_btn_id = f"eliminar_proyect_{project_id}"
        @reactive.Effect
        @reactive.event(input[eliminar_btn_id])
        def eliminar_proyecto_boton():
            print("hola pase, elimino a", eliminar_btn_id)
            create_modal_eliminar_bd()
    
    @reactive.Effect
    @reactive.event(input["eliminar_proyecto_modal"])
    def eliminar_proyeco_modal():
        eliminar_proyecto(global_session.get_id_proyecto())
        # Actualiza proyectos_usuario después de eliminar el proyecto
        # Suponiendo que get_user_projects recarga los proyectos desde la fuente de datos
        proyectos_actualizados = get_user_projects(user_get.get())
        proyectos_usuario.set(proyectos_actualizados)  # Refresca proyectos_usuario con la lista actualizada

        # Actualiza el selector con los proyectos restantes
        ui.update_select(
            "project_select",
            choices={str(proj['id']): proj['name'] for proj in proyectos_actualizados}
        )

        proceso_eliminar.set(True)
        ui.modal_remove()
       
        #return show_selected_project_card(user_get.get(),  global_session.get_id_proyecto())
           

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
                create_navigation_handler('continuar', 'Screen_Desarollo')
                global_user_proyecto.click_en_continuar.set(False)
    @output
    @render.ui
    def devolver_acordeon():
        projects = proyectos_usuario.get()  # Obtiene la lista actual de proyectos
        print("actualizo la lista?", proyectos_usuario.get())
        # Primera condición: si hay proyectos
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
        
        # Segunda condición: si `condition` es verdadera
        elif proceso_eliminar.get():
            return ui.update_select(
        "project_select",
        choices={str(proj['id']): proj['name'] for proj in proyectos_usuario.get()}
        )
        
        # Si ninguna de las condiciones anteriores se cumple
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
