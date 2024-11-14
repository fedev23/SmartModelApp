from shiny import ui
from clases.reactives_name import global_names_reactivos
from clases.global_session import global_session
def create_nav_menu_user(name_suffix):
    return ui.page_navbar(
        ui.nav_control(ui.p(f"Nombre del proyecto: {global_session.get_name_proyecto()}", class_="styled-text")),
        ui.nav_control(ui.p(f"Nombre de la versión: {global_session.get_versiones_name()}", class_="styled-text")),
        ui.nav_control(ui.p(f"Nombre del archivo: {global_names_reactivos.get_name_file_db()}", class_="styled-text")),
            ui.nav_spacer(),
            ui.nav_control(ui.input_dark_mode(mode="light")),
            ui.nav_menu(
                ui.tags.i(class_="fa fa-gear fa-lg"),
                ui.nav_control(
                    ui.input_action_link(f"delete_project_{name_suffix}", "Eliminar proyecto"),
                ),
            ),
            id=f"tab_{name_suffix}",
            title="",
            selected=None,
            inverse=False,
             position='sticky-top',  # Esto hace que se mueva con el contenido
            #bg="night",
            bg="transparent",
            #class_="styled-nav",  # Aplicar la clase personalizada
     
        
        
    )