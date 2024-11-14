from shiny import ui
from global_names import global_name_in_Sample, global_name_desarrollo, global_name_out_of_Sample, global_name_produccion
def create_nav_menu_user(name_suffix):
    return ui.page_navbar(
            ui.nav_control(ui.input_action_link(f"start_{name_suffix}", "Crear proyecto")),
            ui.nav_control(ui.input_action_link(f"version_{name_suffix}", "Crear versión")),
            ui.nav_control(ui.input_action_link(f"boton{name_suffix}", "datos")),
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
            bg="night",
        
        
    )