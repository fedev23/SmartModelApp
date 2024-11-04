from shiny import ui
from global_names import global_name_in_Sample, global_name_desarrollo, global_name_out_of_Sample, global_name_produccion
def create_nav_menu_user(name_suffix):
    return ui.page_fluid(
        ui.navset_bar(
            ui.nav_control(ui.input_action_link(f"start_{name_suffix}", "Comenzar proyecto")),
            ui.nav_menu(
                "Panel de carga",
                ui.nav_control(
                    ui.input_action_link(f"screen_Desarollo_{name_suffix}", f"{global_name_desarrollo}"),
                    ui.input_action_link(f"screen_in_sample_{name_suffix}", f"{global_name_in_Sample}"),
                    ui.input_action_link(f"load_Validacion_{name_suffix}", f"{global_name_out_of_Sample}"),
                    ui.input_action_link(f"screen_Produccion_{name_suffix}", f"{global_name_produccion}")
                ),
            ),
            ui.nav_control(ui.input_action_link(f"ir_modelos_{name_suffix}", "Ejecución")),
            ui.nav_control(ui.input_action_link(f"ir_result_{name_suffix}", "Panel de resultados")),
            
            # Agregar ícono de "settings" sin un título
            ui.nav_menu(
                ui.tags.i(class_="fa fa-gear fa-lg"),  # Ícono de tuerca grande
                ui.nav_control(
                    ui.input_dark_mode(mode="light"),  # Modo de noche/día
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
