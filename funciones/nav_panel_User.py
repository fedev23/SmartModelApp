from shiny import ui
from global_names import global_name_in_Sample, global_name_desarrollo, global_name_out_of_Sample, global_name_produccion
def create_nav_menu_user(name_suffix):
    return ui.page_fluid(
        ui.navset_bar(
            ui.nav_control(ui.input_action_link(f"start_{name_suffix}", f"Crear proyecto")),
            ui.nav_control(ui.input_action_link(f"version_{name_suffix}", f"Crear versión")),
            ui.nav_spacer(),
            ui.nav_control(ui.input_dark_mode(mode="light")),
            ui.nav_menu(
                ui.tags.i(class_="fa fa-gear fa-lg"),  # Ícono de tuerca grande
                ui.nav_control(
                        ui.input_action_link(f"delete_project_{name_suffix}", "Eliminar proyecto"), 
                ),
            ),
            id=f"tab_{name_suffix}",
            title="",
            selected=None,
            inverse=False,
            bg="night",
        ),
    )
